<h1><img src="https://gitlab.com/whoatemybutte7/jsontextmc/-/raw/master/logo.png" width="64" height="64"> JSONTextMC</h1>

JSONTextMC is a tool for converting old Minecraft formatting codes to the modern JSON format.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- [Python >=3.6](https://www.python.org/downloads/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **JSONTextMC**.

```shell script
python3 -m pip install jsontextmc
```

See the package page on PyPi [here](https://pypi.org/project/jsontextmc).

## Usage

### As a module
```pythonstub
import jsontextmc

# returns '["", {"text": "", "color": "red"}, {"text": "Red in Bold", "color": "red", "bold": true}]'
jsontextmc.translate("&c&lRed in Bold", strict=False)

# returns '["", {"text": "Gold, ", "color": "gold"}, {"text": "Gold in Bold, ", "color": "gold", "bold": true}, {"text": "RESET to nothing"}]'
jsontextmc.translate("§6Gold, §lGold in Bold, §rRESET to nothing", sep="§", strict=False) 

# use 1.16 hexidecimal strings
jsontextmc.translate("&#f00000Not quite red.")

# returns a list of all the formatting codes, and their values
print(jsontextmc.CODES)

# returns a list of all the formatting codes, but only the codes themselves
print(jsontextmc.ALL_CODES)
```

### As a script
```shell script
python3 -m jsontextmc "&c&lRed in Bold" --strict false
python3 -m jsontextmc "§6gold, §lgold in bold, §rreset to nothing" --sep "§" --strict false
python3 -m jsontextmc "!^FFAABB!cNice!" --sep "!" --hexchar "^"
```

Use the output in any place where a JsonTextComponent is accepted *(eg. **/tellraw**, **/title**, **.json files**)*.

## Support

Supports all Vanilla Minecraft formatting codes:

- [Color Codes](https://minecraft.gamepedia.com/Formatting_codes#Color_codes)
  - 0 through 9
  - A through F
- Obfuscated
  - K
- Bold
  - L
- Strikethrough 
  - M
- Underlined
  - N
- Italic
  - O
- Reset
  - R
- Hexidecimal
  - 0 through 9
  - A through F
  - Must be 6-wide
  - Must be in the form of `#RRGGBB`, where R, G, B are red, green, blue, respectively.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

If there is an individual issue you would like to bring attention to, please 
[open one here](https://gitlab.com/whoatemybutte7/jsontextmc/issues/new).

## License

Distributed under the [GPLv3](https://choosealicense.com/licenses/gpl-3.0/) license.
*(visit [GNU's website](https://www.gnu.org/licenses/gpl-3.0.en.html))*
