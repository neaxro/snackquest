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

## Flux

To add this app to flux, use the following command:

> Do not forget to export `GITHUB_TOKEN` environment variable!
> `export GITHUB_TOKEN=<app-repo-token>`

Create Image repository

```console
flux create image repository snackquest-repo \
    --image axelnemes/snackquest \
    --interval 5m \
    --export > ./flux/image-repository.yaml
```

Create Image policy

```console
flux create image policy snackquest \
    --image-ref=snackquest-repo \
    --select-alpha=asc \
    --export > ./flux/image-policy.yaml
```

Create Image updater

```console
flux create image update snackquest \
    --interval=5m \
    --git-repo-ref=snackquest \
    --git-repo-path=flux \
    --checkout-branch=main \
    --push-branch=main \
    --author-name=fluxbot \
    --author-email=fluxbot@users.noreply.github.com \
    --commit-template="{{range .Changed.Changes}}{{print .OldValue}} -> {{println .NewValue}}{{end}}" \
    --export > ./flux/flux-system-automation.yaml
```

### Workflow

1. create `feature` branch and work on it.
2. when feature is done, create a PR: `feature` -> `main`.
   1. new image will be built.
   2. new release will be created.
3. if the new feature can go live, merge `main` -> `release/production`.
   1. this need to be fast forward only, so the `main` and `release/production` branches should have the same commit history.
   2. Flux only uses resources located on `release/production` branch.
   3. image tag update will happen on `main`.
