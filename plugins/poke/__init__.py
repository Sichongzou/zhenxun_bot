from nonebot import on_notice
from nonebot.adapters.cqhttp import Bot, PokeNotifyEvent
from nonebot.typing import T_State
from configs.path_config import VOICE_PATH, IMAGE_PATH
import os
from utils.init_result import record, image, poke
from services.log import logger
import random
from utils.utils import CountLimiter
from models.ban_user import BanUser

__plugin_name__ = '戳一戳 [Hidden]'

__plugin_usage__ = '用法：无'

poke__reply = [
    "lsp你再戳？", "连个可爱美少女都要戳的肥宅真恶心啊。",
    "你再戳！", "？再戳试试？", "别戳了别戳了再戳就坏了555", "我爪巴爪巴，球球别再戳了", "你戳你🐎呢？！",
    "那...那里...那里不能戳...绝对...", "(。´・ω・)ん?", "有事恁叫我，别天天一个劲戳戳戳！", "欸很烦欸！你戳🔨呢",
    "?", "再戳一下试试？", "???", "正在关闭对您的所有服务...关闭成功", "啊呜，太舒服刚刚竟然睡着了。什么事？", "正在定位您的真实地址。。。\r\n定位成功。轰炸机已起飞"
]


_clmt = CountLimiter(3)

poke_ = on_notice(priority=5, block=False)


@poke_.handle()
async def _poke_(bot: Bot, event: PokeNotifyEvent, state: T_State):
    if event.self_id == event.target_id:
        _clmt.add(event.user_id)
        if _clmt.check(event.user_id) or random.random() < 0.3:
            rst = ''
            if random.random() < 0.15:
                await BanUser.ban(event.user_id, 1, 60)
                rst = '气死我了！'
            await poke_.finish(rst + random.choice(poke__reply), at_sender=True)
        rand = random.random()
        if rand <= 0.3:
            path = random.choice(['luoli/', 'meitu/'])
            index = random.randint(0, len(os.listdir(IMAGE_PATH + path)))
            result = f'id：{index}' + image(f'{index}.jpg', path)
            await poke_.send(result)
            logger.info(f'USER {event.user_id} 戳了戳我 回复: {result} \n {result}')
        elif 0.3 < rand < 0.6:
            voice = random.choice(os.listdir(VOICE_PATH + 'dinggong/'))
            result = record(voice, "dinggong")
            await poke_.send(result)
            await poke_.send(voice.split('_')[1])
            logger.info(f'USER {event.user_id} 戳了戳我 回复: {result} \n {voice.split("_")[1]}')
        else:
            await poke_.send(poke(event.user_id))

