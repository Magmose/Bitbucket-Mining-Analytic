import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def distribution_comments_category_per_reviewer(data, title):
    # Create a DataFrame from the distribution dictionary
    df_distribution = pd.DataFrame(data).fillna(0).round(2)

    # Save to CSV
    file_path = f'diagrams/{title}.csv'
    df_distribution.to_csv(file_path)

def noprocent_distribution_comments_category_per_reviewer(data, title):
    # Creating a DataFrame from the absolute distribution dictionary
    df_absolute_distribution = pd.DataFrame(data).fillna(0).astype(int)
    
    # Save to CSV
    file_path = f'diagrams/{title}.csv'
    df_absolute_distribution.to_csv(file_path)


def stacked_bar_chart(data, title):
    # Extracting unique names and types from the data structure
    barWidth = 0.7
    categories = list(data.keys())
    names = set()
    for type_group in data.values():
        names.update(type_group.keys())

    types = list(data.keys())

    # Counting occurrences for each name in each type
    counts = {name: [len(data[t].get(name, [])) for t in types] for name in names}

    # Stacked Bar Chart with distinct colors and numbers (excluding zeros)
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    bottom = np.zeros(len(types))
    # color_map = plt.cm.get_cmap('tab10', len(names))  # Color map for distinct colors

    for i, name in enumerate(names):
        counts_by_type = [len(data[t].get(name, [])) for t in types]
        bars = ax.bar(types, counts_by_type, bottom=bottom, label=name, width=barWidth)
        
        # Updating bottom for the next iteration
        new_bottom = bottom + np.array(counts_by_type)

        # Adding numbers centered in each bar segment
        for bar, count, btm, nb in zip(bars, counts_by_type, bottom, new_bottom):
            if count > 1:
                mid = (btm + nb) / 2
                ax.annotate('{}'.format(count),
                            xy=(bar.get_x() + bar.get_width() / 2, mid),
                            xytext=(0, 0),  # no offset
                            textcoords="offset points",
                            ha='center', va='center')

        bottom = new_bottom

    ax.set_xlabel('Categories')
    ax.set_ylabel('Number of Comments')
    ax.set_title(title)
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: int(t[0].split("_")[1]) if "_" in t[0] else t[0]))
    ax.legend(handles, labels)

        
    plt.savefig(f"diagrams/{title}.png")
    plt.close()

# def stacked_bar_chart(data1, data2, title):
#     # Extracting unique names and types from the data structure
#     barWidth = 0.35  # Reduced bar width for accommodating two bars side by side
#     categories = list(set(data1.keys()).union(set(data2.keys())))
#     names = set()
#     for type_group in data1.values():
#         names.update(type_group.keys())
#     for type_group in data2.values():
#         names.update(type_group.keys())

#     types = sorted(categories)

#     # Counting occurrences for each name in each type
#     counts1 = {name: [len(data1[t].get(name, [])) for t in types] for name in names}
#     counts2 = {name: [len(data2[t].get(name, [])) for t in types] for name in names}

#     # Stacked Bar Chart with distinct colors and numbers (excluding zeros)
#     fig, ax = plt.subplots(figsize=(10, 6))
#     bottom1 = np.zeros(len(types))
#     bottom2 = np.zeros(len(types))
#     color_map = plt.cm.get_cmap('tab10', len(names))  # Color map for distinct colors

#     for i, name in enumerate(names):
#         counts_by_type1 = [len(data1[t].get(name, [])) for t in types]
#         counts_by_type2 = [len(data2[t].get(name, [])) for t in types]
        
#         # Bars for data1
#         bars1 = ax.bar(np.array(types) - barWidth/2, counts_by_type1, bottom=bottom1, label=name, color=color_map(i), width=barWidth)
#         # Bars for data2
#         bars2 = ax.bar(np.array(types) + barWidth/2, counts_by_type2, bottom=bottom2, color=color_map(i), width=barWidth, alpha=0.5)

#         # Updating bottom for the next iteration
#         bottom1 += np.array(counts_by_type1)
#         bottom2 += np.array(counts_by_type2)

#     ax.set_xlabel('Categories')
#     ax.set_ylabel('Number of Comments')
#     ax.set_title(title)
#     handles, labels = ax.get_legend_handles_labels()
#     ax.legend(handles, labels, loc='upper left')

#     plt.savefig(f"diagrams/{title}.png")
#     plt.close()

def generate_calculate_percentage_contributions(data_set, title):
    df = pd.DataFrame(data_set)
    df = df.fillna(0)
    df = df.round(2)
    file_path = f'diagrams/{title}.csv'
    df.to_csv(file_path)


def percentage_contributions_pie_chart(data_set, title):
    labels = list(data_set.keys())
    sizes = list(data_set.values())

    # Distinct colors for each segment
    colors = plt.cm.Paired(range(len(labels)))

    # Create a pie chart with a legend
    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    plt.title(title)
    plt.legend(labels, title="Individuals", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.savefig(f"diagrams/{title.replace(' ','')}.png")
    plt.close()

def _add_labels(bars):
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

def generate_bar_chart(data1, data2, title):
    barWidth = 0.3
    categories = list(data1.keys())
    r1 = np.arange(len(categories))
    r2 = [x + barWidth for x in r1]

    bars1 = plt.bar(r1, [len(data1[cat]) for cat in categories], width=barWidth, label='bamk')

    bars2 = plt.bar(r2, [len(data2[cat]) for cat in categories], width=barWidth, label='alkl')

    plt.xlabel('Categories')
    plt.ylabel('Number of Comments')
    plt.title(title)
    plt.xticks([r + barWidth/2 for r in range(len(categories))], categories)

    plt.legend()
    _add_labels(bars1)
    _add_labels(bars2)

    fig = plt.gcf()  # Get the current figure
    print("Current figure size:", fig.get_size_inches())

    plt.savefig(f"diagrams/{title.replace(' ','')}.png")
    plt.close()