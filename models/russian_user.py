from services.db_context import db
from typing import List


class RussianUser(db.Model):
    __tablename__ = 'russian_users'

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)
    win_count = db.Column(db.Integer(), default=0)
    fail_count = db.Column(db.Integer(), default=0)
    make_money = db.Column(db.Integer(), default=0)
    lose_money = db.Column(db.Integer(), default=0)

    _idx1 = db.Index('russian_group_users_idx1', 'user_qq', 'group_id', unique=True)

    @classmethod
    async def ensure(cls, user_qq: int, group_id: int) -> 'RussianUser':
        user = await cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        ).with_for_update().gino.first()
        return user or await cls.create(
            user_qq=user_qq,
            group_id=group_id
        )

    @classmethod
    async def add_count(cls, user_qq: int, group_id: int, itype: str) -> bool:
        try:
            user = await cls.query.where(
                (cls.user_qq == user_qq) & (cls.group_id == group_id)
            ).with_for_update().gino.first()
            if not user:
                user = await cls.create(
                    user_qq=user_qq,
                    group_id=group_id
                )
            if itype == 'win':
                await user.update(
                    win_count=user.win_count + 1,
                ).apply()
            elif itype == 'lose':
                await user.update(
                    fail_count=user.fail_count + 1,
                ).apply()
            return True
        except Exception:
            return False

    @classmethod
    async def money(cls, user_qq: int, group_id: int, itype: str, count: int) -> bool:
        try:
            user = await cls.query.where(
                (cls.user_qq == user_qq) & (cls.group_id == group_id)
            ).with_for_update().gino.first()
            if not user:
                user = await cls.create(
                    user_qq=user_qq,
                    group_id=group_id
                )
            if itype == 'win':
                await user.update(
                    make_money=user.make_money + count,
                ).apply()
            elif itype == 'lose':
                await user.update(
                    lose_money=user.lose_money + count,
                ).apply()
            return True
        except Exception:
            return False

    @classmethod
    async def all_user(cls, group_id: int) -> List['RussianUser']:
        users = await cls.query.where(
            (cls.group_id == group_id)
        ).gino.all()
        return users

