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
From the given balance and menu list calculates the optimal order to leave as less money on the card as possible.

```sh
python3 snackquest.py balance menu.yaml
```
Example how to calculate best order list:
```sh
python3 snackquest/snackquest.py 1300 examples/example01.yaml
```
Output:
```sh
user@ubuntu:~/snackquest$ python3 snackquest/snackquest.py 2300 examples/example01.yaml

           Solution #1
┏━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃ Snack Options  ┃ Count ┃ Price ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━┩
│ Twix           │ 5     │   280 │
│ Snickers, Mars │ 3     │   300 │
├────────────────┼───────┼───────┤
│                │ Total │  2300 │
└────────────────┴───────┴───────┘
       Final balance: 0 JMF

           Solution #2
┏━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃ Snack Options  ┃ Count ┃ Price ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━┩
│ Twix           │ 6     │   280 │
│ Bounty         │ 1     │   320 │
│ Snickers, Mars │ 1     │   300 │
├────────────────┼───────┼───────┤
│                │ Total │  2300 │
└────────────────┴───────┴───────┘
       Final balance: 0 JMF

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