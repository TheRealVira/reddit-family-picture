# reddit-family-picture
Generate a family picture of a subreddit moderation team.

## Optional Parameters
| Parameter  | Default | Description |
| ------------- | ------------- | ------------- |
| `subreddit`  | `redditdev`  | Subreddit selection  |
| `sub_dir`  | `./sub/`  | main subreddit directory  |

## Run example
```
$> python reddit_family_picture.py
Querying moderators of redditdev
Performing query as: reddit_user
Queried moderators include:
- u/ketralnis
- u/spez
- u/jedberg
- u/kn0thing
- u/KeyserSosa
- u/chromakode
- u/bboe
- u/taylorkline
- u/Stuck_In_the_Matrix
- u/lift_ticket83
- u/lurker
- u/thephilthe
- u/ac_oatmeal
- u/pl00h
===
Generating family picture...
===
Saving family_picture.png ...
Done!
```
# Resuslt
![result image](./content/family_picture.png)