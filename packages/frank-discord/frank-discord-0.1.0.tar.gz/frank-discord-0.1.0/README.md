# Frank
## Description
Playing around with creating a Discord bot is a fun pass-time, and a good way to learn a programming language. Sadly,
however, discord.py can be a little hard to work with at times. That's when I got the idea to create Frank. The goal of
Frank is to make creating Discord bots easier. It handles all the bot-related stuff in the background, so you can focus
on writing the functionality of the bot itself, not how the bot works/interacts with Discord.

Frank works by dividing the bot into modules. Each module has its own prefix, commands, and daemons. Frank handles
routing the Discord commands to their respective functions.

## Example Module
In this section, I've written an example module for you, to understand the basic mechanics behind Frank.

```python
import frank

class ExampleMod(frank.Module):
    PREFIX = 'examp'
    NAME = 'example'
    HELP = 'an example module'
```

This first part shows the three important variables in any module.
- PREFIX defines the string used to use the commands defined in this module. This means you can use the module as such
  inside your Discord server:
  ```
  fr examp [NAME_OF_COMMAND] [ARGS]
  ```
  With fr being the default prefix for Frank (can be overwritten). As you define more modules, they should all have a
  unique prefix. This is how Frank's modular system works, and any modules added to the list will automatically be
  picked up by Frank. The PREFIX value can also be list, allowing for multiple prefixes: for example a long,
  description one, and a short, easy to type one (e.g. minecraft and mc).

```python
    def pre_start(self):
        self.some_var = 'a value needed for working'
```

The pre_start function is where you define any variables which should be created before any daemons are started or
commands are run. I don't recommend overwriting `__init__`, as this might break compatibility with future versions of
Frank.

```python
    @frank.command('command', help_str='a small description of the command')
    async def some_command(self, cmd, author, channel, mid):
        # do some stuff
        pass

    @frank.daemon()
    async def some_daemon(self):
        while True:
            # do some stuff
            pass

    @frank.default()
    async def default_cmd(self):
        # do some default action
        pass
```

These three decorators are the bread and butter of Frank. Let's break them down:
- `frank.command` defines a command. The first argument is its keyword, which will be used to execute the command. The
  help_str value is used in the help command, to show some information about the module. The syntax is the same as
  before:
  ```
  fr examp command [ARGS]
  ```
  This is how you can define as many Discord commands as you want, without needing to know how to parse the messages
  etc. Each command gets the `author`, `channel`, and `id` of the message. The `cmd` variable contains all the arguments passed
  to the command.
- `frank.daemon` defines a daemon, a process that should run in the background for as long as the bot is active. It
  should contain a while loop and preferably a sleep function using `asyncio.sleep()` (there are plans to improve this
  behavior). Because a daemon is just a method of the module class, it has access to all class variables, including
  those defined in `pre_start`.
- `frank.default` defines the command that should be run if the module is called without explicitely giving a command.
  For example, if you call `fr examp` without specifying a command, it will run the default command. This is useful for
  making a command that's used very often easier to execute.
