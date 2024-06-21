from rsserpent_rev.models import Persona, Plugin

from . import group

plugin = Plugin(
    name="rsserpent-plugin-douban",
    author=Persona(
        name="m0wong",
        link="https://github.com/m0wong",
        email="m0wongxx@gmail.com",
    ),
    prefix="/douban",
    repository="https://github.com/m0wong/rsserpent-plugin-douban",
    routers={group.path: group.provider},
)
