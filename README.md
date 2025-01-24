![Snackquest](assets/SnackquestBanner.png)
# :chocolate_bar: snackquest
<p style="text-align:center;font-size:22px">
<b>S</b>nacks <b>N</b>earest <b>A</b>pproach to <b>C</b>alculate <b>K</b>oin <b>Q</b>uota <b>U</b>tilizing <b>E</b>fficient <b>S</b>election <b>T</b>actics
</p>

## :hammer_and_wrench: Installation
1. Clone the repo
    ```sh
    git clone https://github.com/neaxro/snackquest.git
    ```
2. Install packages
    ```sh
    make packages 
    ```
    or
    
    ```sh
    pip install -r requirements.txt
    ```

## :dart: Usage
From the given budget and menu list calculates the optimal order to leave as less money on the card as possible.

```sh
python3 snackquest.py budget menu.yaml
```
Example how to calculate best order list:
```sh
python3 snackquest/snackquest.py 1300 examples/example01.yaml
```
Output:
```sh
user@ubuntu:~/snackquest$ python3 snackquest/snackquest.py 2300 examples/example01.yaml

         The Optimal Solution          
┏━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ Snack Options  ┃ Count ┃ Unit price ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ Snickers       │ 0     │        300 │
│ Twix           │ 8     │        280 │
│ Bounty         │ 0     │        320 │
│ Mars           │ 0     │        290 │
├────────────────┼───────┼────────────┤
│ Total          │ 8     │       2240 │
│ Remaining      │       │         60 │
├────────────────┼───────┼────────────┤
│ Initial budget │       │       2300 │
└────────────────┴───────┴────────────┘
         Initial budget: 2300

user@ubuntu:~/snackquest$
```
## :bookmark_tabs: Menu file
The program needs a menu file which contains all of the Candy Machine information. The only valid formatum is **.yaml/yml**.

Example for the menu structure:
```yaml
---
items:
  - name: snack_name    # Name of the snack
    price: 300          # Price of the snack
    desired: 0          # Minimum amount you want (default: 0)
    available: True     # Is the snack available
    ...
```
> If you do not want the snack to be calculated set the `available` attribute to `False`.

> More menu item list examples in the `examples` folder.