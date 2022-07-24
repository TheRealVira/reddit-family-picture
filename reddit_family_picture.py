# importing the module
import praw, urllib, os, shutil, config, glob, random, PIL, math, itertools, argparse
from PIL import Image, ImageDraw, ImageFont
from random import randrange

# Defining argument parser
parser = argparse.ArgumentParser(
    description="Generate a family picture of a subreddit moderation team."
)
parser.add_argument("--subreddit", help="subreddit selection", default="redditdev")
parser.add_argument("--sub_dir", help="main subreddit directory", default="./sub/")

# Parsing/Fetching arguments
args = parser.parse_args()


# Main entry point
def main(subreddit, sub_dir):
    sub_dir = sub_dir + subreddit + "/"
    prepare_directories(sub_dir)

    # creating an authorized reddit instance
    reddit = praw.Reddit(
        client_id=config.secrets["client_id"],
        client_secret=config.secrets["client_secret"],
        user_agent=config.user_agent,
        password=config.secrets["password"],
        username=config.secrets["username"],
    )

    # query all moderators and safe data
    query_moderators(reddit, subreddit, sub_dir)

    # generating the final family picture
    generate_family_picture(subreddit, sub_dir)


# Setting up subreddit directories.
# This will store all moderator avatars and the final family picture.
def prepare_directories(sub_dir):
    if os.path.exists(sub_dir):
        shutil.rmtree(sub_dir)
    os.makedirs(sub_dir + "result/")


# Querry moderators of a specific subreddit and safe all avatars
# as seperate png files.
def query_moderators(reddit, subreddit, sub_dir):
    print("Querying moderators of " + subreddit)
    print("Performing query as: " + reddit.user.me().name)
    print("Queried moderators include:")

    # Query through moderators of a sub
    for moderator in reddit.subreddit(subreddit).moderator():

        # instantiating the Redditor class
        redditor = reddit.redditor(moderator)

        print("- u/" + str(redditor.name))

        # retrieve the avatar
        urllib.request.urlretrieve(
            redditor.icon_img, sub_dir + "/" + redditor.name + ".png"
        )


# Generate a family picture based on the subreddit name and moderator
# avatars
def generate_family_picture(subreddit, sub_dir):
    print("===")
    print("Generating family picture...")
    family_picture_canvas = PIL.Image.new(mode="RGBA", size=(1920, 1080))

    draw = ImageDraw.Draw(family_picture_canvas)
    font = ImageFont.truetype("arial.ttf", 140)

    W, H = family_picture_canvas.size
    w, h = draw.textsize(subreddit, font=font)

    avatars = glob.glob(sub_dir + "*.png")
    index = 0

    for pos_x, pos_y in get_n_points_on_curve(len(avatars), W * 0.8, H / 2):
        avatar_im = Image.open(avatars[index]).convert("RGBA")
        family_picture_canvas.paste(
            avatar_im, (int(pos_x + W * 0.05), int(H / 2 - pos_y)), avatar_im
        )
        index += 1

    draw.text(
        ((W - w) / 2, H - h - 150),
        subreddit,
        fill="black",
        stroke_width=5,
        stroke_fill="white",
        font=font,
    )

    print("===")
    print("Saving family_picture.png ...")
    family_picture_canvas.save(sub_dir + "result/family_picture.png")
    print("Done!")


# Calculate n points on a sinus curve with a defined length and height
# Points appear from the middle to the right and then from the middle
# to the left. That way avatars overlap based on y and not based on x.
def get_n_points_on_curve(n, curve_length, curve_height):
    sector_length = curve_length / (n - 1)
    halfindex = int(n / 2)

    for i in itertools.chain(range(halfindex, n), reversed(range(0, halfindex))):
        x = sector_length * i
        y = math.sin((x / curve_length) * math.pi) * curve_height
        yield (x, y)


if __name__ == "__main__":
    main(subreddit=args.subreddit, sub_dir=args.sub_dir)
