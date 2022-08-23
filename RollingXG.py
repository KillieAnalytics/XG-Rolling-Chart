import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from highlight_text import fig_text
from PIL import Image

def create_rolling_xg(matches, most_used_team, home_colour, away_colour, game_split, event_list, image_file):
    sorted_matches = matches.sort_values('Date', ascending=True)

    xg_for = sorted_matches.loc[sorted_matches['Team'] == most_used_team][['Date', 'xG']]
    xg_for = xg_for.rename(columns={'xG': 'xGFor'})

    xg_against = sorted_matches.loc[sorted_matches['Team'] != most_used_team][['Date', 'xG']]
    xg_against = xg_against.rename(columns={'xG': 'xGAgainst'})

    xg_rolling = xg_for.merge(xg_against, on=['Date'])

    y_for = xg_for['xGFor'].reset_index(drop = True)
    y_against = xg_against['xGAgainst'].reset_index(drop = True)

    x = pd.Series(range(len(xg_rolling)))

    y_for = y_for.rolling(window = 10, min_periods = 0).mean()
    y_against = y_against.rolling(window = 10, min_periods = 0).mean()

    fig = plt.figure(figsize=(4.5, 2.5), dpi = 300, facecolor = "#252827")
    ax = plt.subplot(111, facecolor = "#252827")

    # Remove top & right spines and change the color.
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("grey")

    # Set the grid
    ax.grid(
        visible = True, 
        lw = 0.75,
        ls = ":",
        color = "lightgrey"
    )

    line_1 = ax.plot(x, y_for, zorder = 4, color=home_colour)
    line_2 = ax.plot(x, y_against, zorder = 4, color=away_colour)

    ax.set_ylim(0)
    # Add a line to mark the division between seasons
    for title, date in event_list:
        ax.plot(
            [date,date], # 38 games per season
            [ax.get_ylim()[0], ax.get_ylim()[1]],
            ls = ":",
            lw = 1.25,
            color = "grey",
            zorder = 2
        )

        ax.annotate(
            xy = (date, .1),
            xytext = (20, 10),
            textcoords = "offset points",
            text = title,
            size = 3,
            color = "grey",
            arrowprops=dict(
                arrowstyle="->", shrinkA=0, shrinkB=5, color="grey", linewidth=0.50,
                connectionstyle="angle3,angleA=50,angleB=-30"
            ) # Arrow to connect annotation
        )

    # Fill between
    ax.fill_between(
        x, 
        y_against,
        y_for, 
        where = y_for >= y_against, 
        interpolate = True,
        alpha = 0.70,
        zorder = 3,
        color=home_colour
    )

    ax.fill_between(
        x, 
        y_against,
        y_for, 
        where = y_against > y_for, 
        interpolate = True,
        alpha = 0.70,
        color=away_colour
    )

    # Customize the ticks to match spine color and adjust label size.
    ax.tick_params(
        color = "grey", 
        length = 5, 
        which = "major", 
        labelsize = 6,
        labelcolor = "grey",
        zorder = 3
    )

    # Set x-axis major tick positions to only 19 game multiples.
    ax.xaxis.set_major_locator(ticker.MultipleLocator(game_split))
    # Set y-axis major tick positions to only 0.5 xG multiples.
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))

    # Title and subtitle for the legend
    fig_text(
        x = 0.12, y = 1.1,
        s = most_used_team,
        color = "white",
        weight = "bold",
        size = 10,
        annotationbbox_kw={"xycoords": "figure fraction"}
    )

    fig_text(
        x = 0.12, y = 1.02,
        s = "Expected goals <created> and <conceded> | 10-match rolling average",
        highlight_textprops = [
            {"color": home_colour, "weight": "bold"},
            {"color": away_colour, "weight": "bold"}
        ],
        color = "white",
        size = 6,
        annotationbbox_kw={"xycoords": "figure fraction"}
    )

    if image_file is not None:
        logo_ax = fig.add_axes([0.75, .99, 0.25, 0.25], zorder=1)
        club_icon = Image.open(image_file)
        logo_ax.imshow(club_icon)
        logo_ax.axis("off")

    fn = most_used_team + "RollingXG.png"
    plt.savefig(fn, bbox_inches='tight')
    return fn, fig