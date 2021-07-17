import json
import os

from package.bot import SoundReactor


def main() -> None:
    with open('config.json', 'r') as fp:
        config = json.load(fp)

    token: str = os.environ.get('SOUND_REACTOR_TOKEN',
                                config['token'])

    bot = SoundReactor(**config)
    bot.run(token)


if __name__ == '__main__':
    main()
