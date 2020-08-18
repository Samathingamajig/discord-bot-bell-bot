# Bell Bot

This is a discord bot in python that pings `@bells` whenever a bell would ring at school. This reminds students to join their next zoom meeting since we are doing virtual learning this year.


| Command | Args       | Aliases                             | What it do                                                                           | Permissions   |
| :---:   | :---       | :---                                | :---:                                                                                |:---:          |
| help    | n/a        | n/a                                 | prints the help message of each command                                              | @everyone     |
| block   | n/a        | ab, todays-block, a/b, aorbday, 🆎 | reacts to the sent message with either 🅰️, 🅱️, or ❌, depending on the current day  | @everyone     |
| block   | month, day | ab, todays-block, a/b, aorbday, 🆎 | reacts to the sent message with either 🅰️, 🅱️, or ❌, depending on the date entered | @everyone     |
| restart | n/a        | rs, you-stupid                      | restarts the bot and reloads config and data files                                   | Administrator |

# Important

If you decide to clone this and change this for your discord server, you need to change some things:

---
Create a file "secrets.py" and store your bot api token there like this:
```python
CLIENT_SECRET = "STRING_OF_API_TOKEN"
```

---
* In ./config.yml: (everything is described more in the yml file) (to get the ID's, go to Settings > Appearance > Developer Mode = True)
1. Log Channel ID
2. Announcements Channel ID
3. Pinged Role ID
4. User Timezone
---
* In ./block-schedule.yml: (change this to your "A" day or "B" day schedule)

Format:
```yml
MONTH:
  DAY: A/B
  DAY: A/B
MONTH:
  DAY: A/B
  DAY: A/B
```
Example:
```yml
8:
  13: A
  14: B
9:
  9: A
  10: B
```
---
* In ./bell-schedule.json:

Example:
```json
[
  {
    "hour": 8,
    "minute": 55,
    "period": 1,
    "message": "default",
    "type": "starting"   
  },
  {
    "hour": 9,
    "minute": 0,
    "period": 1,
    "message": "default",
    "type": "tardy"
  },
  {
    "hour": 10,
    "minute": 30,
    "period": 2,
    "message": "default",
    "type": "passing"
  },
  {
    "hour": 12,
    "minute": 5,
    "period": "lunch",
    "message": "dab on 'em haters, it's lunch time!",
    "type": ""
  }
]
```
Supported periods:
* 1-4, anything else

Supported messages:
* default, anything else

Supported types:
* starting, passing, tardy, [blank]