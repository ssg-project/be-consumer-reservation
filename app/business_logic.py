from app.mysql_connect import insert_reservation 
from app.redis_client import redis_client
from app.ws_connect import ws_send_success, ws_send_fail
import logging

logger = logging.getLogger(__name__)

async def process_reservation(message):
    """
    티켓 예약 요청을 처리하는 함수 (Redis 및 DB 활용)
    """

    logger.info('process_reservation : start')

    user_id = message.get('user_id')
    concert_id = message.get('concert_id')

    # Redis 키 정의
    seat_reserved_count_key = f"concert:{concert_id}:seat_reserved_count"
    seat_all_count_key = f"concert:{concert_id}:seat_all_count"
    user_reserved_key = f"concert:{concert_id}:user:{user_id}:reserved"
    lock_key = f"lock:concert:{concert_id}"

    # 이미 예약된 사용자인지 확인
    if redis_client.get(user_reserved_key):
        logger.info(f"User {user_id} has already reserved a ticket!")

        await ws_send_fail(user_id, concert_id, "already reserved a ticket")
        return

    # Redis에서 현재 예약 수와 좌석 제한 확인
    seat_reserved_count = redis_client.get(seat_reserved_count_key)
    seat_all_count = redis_client.get(seat_all_count_key)

    if seat_reserved_count is None or seat_all_count is None:
        logger.info(f"Concert {concert_id} data is missing in Redis. Aborting...")
        
        await ws_send_fail(user_id, concert_id, "concert data is missing")
        return

    seat_reserved_count = int(seat_reserved_count)
    seat_all_count = int(seat_all_count)

    # 좌석이 이미 꽉 찬 경우
    if seat_reserved_count >= seat_all_count:
        logger.info(f"Concert {concert_id} is fully booked!")

        await ws_send_fail(user_id, concert_id, "concert is fully booked")
        return

    # Redis 잠금 설정
    if not redis_client.set(lock_key, user_id, nx=True, ex=10):
        logger.info(f"Concert {concert_id} is already locked!")

        await ws_send_fail(user_id, concert_id, "unable to acquire lock")
        return

    try:
        # Redis 예약 수 증가
        new_reserved_count = redis_client.incr(seat_reserved_count_key)

        # 좌석 초과 여부 재확인 (경쟁 상태에서 마지막 체크)
        if new_reserved_count > seat_all_count:
            logger.info(f"Race condition: Concert {concert_id} is fully booked after increment.")

            redis_client.decr(seat_reserved_count_key)  # 롤백
            await ws_send_fail(user_id, concert_id, "concert is fully booked")
            return

        # DB에 예약 정보 저장
        insert_reservation(user_id, concert_id)

        # 유저 예약 상태 Redis에 기록
        logger.info(f"User {user_id} successfully reserved ticket {concert_id}!")
        redis_client.set(user_reserved_key, "true", ex=3600)  # 1시간 TTL
        await ws_send_success(user_id, concert_id)

    except Exception as e:
        logger.info(f"Error processing reservation: {e}")
        redis_client.decr(seat_reserved_count_key)
        await ws_send_fail(user_id, concert_id, f"{e}")

    finally:
        redis_client.delete(lock_key)
