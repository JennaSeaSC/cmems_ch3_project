# src/cohort_summary_extractor.py

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from project_paths import OUTPUTS_DIR, COHORTS_DIR

# CONFIG
cohort_tag = "2014-12_multi"
regions = ["Bight_Core", "Transition_Zone", "North_Offshore"]

# Define region bounds for stranding filtering
region_bounds = {
    "Bight_Core": {"lat": (32.5, 34.5), "lon": (-121.5, -117.5)},
     "Transition_Zone": {"lat": (34.5, 36), "lon": (-122, -119)},
     "North_Offshore": {"lat": (36, 47), "lon": (-125, -122)}
 } # decision-making time about hard boundaries (model reproducibility vs expansion for obs strandings)

# Color + size mappings
species_colors = {"CM": "#2a5d38", "LO": "#b1a700", "CC": "#a65428"}
size_mapping = {"immature": 50, "adult": 120}

# Load cohort stranding file
cohort_file = os.path.join(COHORTS_DIR, f"{cohort_tag}_stranding.csv")
df_strand = pd.read_csv(cohort_file)
df_strand['date'] = pd.to_datetime(df_strand['date'], format="%m/%d/%Y")

for region_name in regions:
    # Load rolling fingerprint file
    input_dir = os.path.join(OUTPUTS_DIR, cohort_tag, "cohort_rolling_fingerprint")
    input_file = os.path.join(input_dir, f"{cohort_tag}_{region_name}_rolling_fingerprint.csv")

    if not os.path.exists(input_file):
        print(f"⚠️ Missing rolling fingerprint file for: {region_name} — skipping.")
        continue

    df = pd.read_csv(input_file)
    df['date'] = pd.to_datetime(df['date'])

    threshold_temp = 14.5
    mean_sst = df['mean_sst_c'].mean()
    max_sst = df['mean_sst_c'].max()
    df['cooling_load'] = np.maximum(0, threshold_temp - df['mean_sst_c'])
    cdd = df['cooling_load'].sum()
    sub_thresh_days = (df['mean_sst_c'] < threshold_temp).sum()

    days_since_start = (df['date'] - df['date'].min()).dt.days
    slope, intercept = np.polyfit(days_since_start, df['mean_sst_c'], 1)

    onset_candidates = df[df['mean_sst_c'] < threshold_temp]
    onset_date = onset_candidates['date'].min() if not onset_candidates.empty else np.nan

    summary = pd.DataFrame({
        'cohort_tag': [cohort_tag],
        'region': [region_name],
        'mean_sst': [mean_sst],
        'max_sst': [max_sst],
        'cdd': [cdd],
        'sub_threshold_days': [sub_thresh_days],
        'cooling_slope': [slope],
        'cooling_onset_date': [onset_date]
    })

    summary_dir = os.path.join(OUTPUTS_DIR, cohort_tag, "cohort_summary")
    os.makedirs(summary_dir, exist_ok=True)
    summary_file = os.path.join(summary_dir, f"{cohort_tag}_{region_name}_summary.csv")
    summary.to_csv(summary_file, index=False)
    print(f"✅ Summary saved → {summary_file}")

    # Filter strandings in this region
    strandings_region = df_strand[df_strand['region'] == region_name].copy()
    strandings_region['mean_sst_c'] = strandings_region['date'].map(df.set_index('date')['mean_sst_c'])
    colors = strandings_region['species'].map(species_colors).fillna("gray")
    sizes = strandings_region['age_class'].map(size_mapping).fillna(80)

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['mean_sst_c'], color='skyblue', label='Daily Mean SST')
    plt.plot(df['date'], df['rolling_mean'], color='blue', label='5-day Rolling Mean')
    plt.axhline(mean_sst, color='gray', linestyle='--', label='Window Mean')
    plt.axhline(threshold_temp, color='red', linestyle=':', label=f'{threshold_temp}°C Threshold')
    if pd.notnull(onset_date):
        plt.axvline(onset_date, color='orange', linestyle='--', label='Cooling Onset')

    # Plot strandings
    plt.scatter(
        strandings_region['date'],
        strandings_region['mean_sst_c'],
        s=sizes,
        c=colors,
        edgecolors="black",
        alpha=0.9,
        zorder=5
    )

    # Legends
    species_legend = [
        Line2D([0], [0], marker='o', color='w', label='Green (CM)', markerfacecolor=species_colors['CM'], markersize=10, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Olive Ridley (LO)', markerfacecolor=species_colors['LO'], markersize=10, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Loggerhead (CC)', markerfacecolor=species_colors['CC'], markersize=10, markeredgecolor='black'),
    ]
    age_legend = [
        Line2D([0], [0], marker='o', color='w', label='Immature', markerfacecolor='gray', markersize=6, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Adult', markerfacecolor='gray', markersize=12, markeredgecolor='black'),
    ]

    legend1 = plt.legend(handles=species_legend, title="Species", loc='lower right')
    legend2 = plt.legend(handles=age_legend, title="Age Class", loc='lower center')
    plt.gca().add_artist(legend1)

    # SST line legend (mean, rolling, threshold, onset)
    smt_legend = plt.legend(
        loc='upper right',  # Top right corner
        frameon=True
    )
    plt.gca().add_artist(smt_legend)

    plt.title(f"Cohort SST Summary: {cohort_tag} ({region_name})")
    plt.ylabel("SST (°C)")
    plt.xlabel("Date")
    plt.grid(True)
    plt.tight_layout()

    plot_file = os.path.join(summary_dir, f"{cohort_tag}_{region_name}_summary_plot.png")
    plt.savefig(plot_file, dpi=150)
    plt.show()
    plt.close()

    print(f"🎯 Summary plot saved → {plot_file}")


# # src/cohort_summary_extractor.py

# import os
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.lines import Line2D
# from project_paths import OUTPUTS_DIR, COHORTS_DIR

# # CONFIG
# cohort_tag = "2014-12_multi"
# regions = ["Bight_Core", "Transition_Zone", "North_Offshore"]
# threshold_temp = 14.5

# # Define region bounds for stranding filtering
# region_bounds = {
#     "Bight_Core": {"lat": (32.5, 34.5), "lon": (-121.5, -117.5)},
#     "Transition_Zone": {"lat": (34.5, 36), "lon": (-122, -119)},
#     "North_Offshore": {"lat": (36, 46), "lon": (-125, -122)}
# }

# # Color + size mapping
# species_colors = {"CM": "#2E8B57", "LO": "#A2A85D", "CC": "#A0522D"}  # deep green, olive-yellow, loggerhead brown
# size_map = {"immature": 50, "adult": 120}

# # Load all strandings
# cohort_file = os.path.join(COHORTS_DIR, f"{cohort_tag}_stranding.csv")
# strandings_df = pd.read_csv(cohort_file)
# strandings_df['date'] = pd.to_datetime(strandings_df['date'], format="%m/%d/%Y")

# # Process each region
# for region_name in regions:
#     input_dir = os.path.join(OUTPUTS_DIR, cohort_tag, "cohort_rolling_fingerprint")
#     input_file = os.path.join(input_dir, f"{cohort_tag}_{region_name}_rolling_fingerprint.csv")

#     if not os.path.exists(input_file):
#         print(f"⚠️ Missing rolling fingerprint file for: {region_name} — skipping.")
#         continue

#     df = pd.read_csv(input_file)
#     df['date'] = pd.to_datetime(df['date'])

#     mean_sst = df['mean_sst_c'].mean()
#     max_sst = df['mean_sst_c'].max()
#     df['cooling_load'] = np.maximum(0, threshold_temp - df['mean_sst_c'])
#     cdd = df['cooling_load'].sum()
#     sub_thresh_days = (df['mean_sst_c'] < threshold_temp).sum()
#     days_since_start = (df['date'] - df['date'].min()).dt.days
#     slope, intercept = np.polyfit(days_since_start, df['mean_sst_c'], 1)
#     onset_candidates = df[df['mean_sst_c'] < threshold_temp]
#     onset_date = onset_candidates['date'].min() if not onset_candidates.empty else np.nan

#     # === Filter strandings to this region ===
#     lat_min, lat_max = region_bounds[region_name]["lat"]
#     lon_min, lon_max = region_bounds[region_name]["lon"]
#     regional_strandings = strandings_df[
#         (strandings_df['lat'] >= lat_min) & (strandings_df['lat'] <= lat_max) &
#         (strandings_df['lon'] >= lon_min) & (strandings_df['lon'] <= lon_max)
#     ]

#     # === Save summary CSV ===
#     summary = pd.DataFrame({
#         'cohort_tag': [cohort_tag],
#         'region': [region_name],
#         'mean_sst': [mean_sst],
#         'max_sst': [max_sst],
#         'cdd': [cdd],
#         'sub_threshold_days': [sub_thresh_days],
#         'cooling_slope': [slope],
#         'cooling_onset_date': [onset_date]
#     })

#     summary_dir = os.path.join(OUTPUTS_DIR, cohort_tag, "cohort_summary")
#     os.makedirs(summary_dir, exist_ok=True)
#     summary_file = os.path.join(summary_dir, f"{cohort_tag}_{region_name}_summary.csv")
#     summary.to_csv(summary_file, index=False)
#     print(f"✅ Summary saved → {summary_file}")

#     # === Plot ===
#     plt.figure(figsize=(12, 6))
#     plt.plot(df['date'], df['mean_sst_c'], color='skyblue', label='Daily Mean SST')
#     plt.plot(df['date'], df['rolling_mean'], color='blue', label='5-day Rolling Mean')
#     plt.axhline(mean_sst, color='gray', linestyle='--', label='Window Mean')
#     plt.axhline(threshold_temp, color='red', linestyle=':', label=f'{threshold_temp}°C Threshold')
#     if pd.notnull(onset_date):
#         plt.axvline(onset_date, color='orange', linestyle='--', label='Cooling Onset')

#     # === Plot strandings as dots ===
#     stranding_colors = regional_strandings['species'].map(species_colors).fillna("gray")
#     stranding_sizes = regional_strandings['age_class'].map(size_map).fillna(80)
#     y_dot_level = threshold_temp - 0.1  # offset to keep dots from overlapping lines

#     plt.scatter(
#         regional_strandings['date'],
#         np.full_like(regional_strandings['date'], y_dot_level),
#         c=stranding_colors,
#         s=stranding_sizes,
#         edgecolors='black',
#         alpha=0.9,
#         zorder=5
#     )

#     # === Legends ===
#     species_legend = [
#         Line2D([0], [0], marker='o', color='w', label='Green (CM)',
#                markerfacecolor=species_colors['CM'], markeredgecolor='black', markersize=10),
#         Line2D([0], [0], marker='o', color='w', label='Olive Ridley (LO)',
#                markerfacecolor=species_colors['LO'], markeredgecolor='black', markersize=10),
#         Line2D([0], [0], marker='o', color='w', label='Loggerhead (CC)',
#                markerfacecolor=species_colors['CC'], markeredgecolor='black', markersize=10),
#     ]
#     age_legend = [
#         Line2D([0], [0], marker='o', color='w', label='Immature',
#                markerfacecolor='gray', markeredgecolor='black', markersize=6),
#         Line2D([0], [0], marker='o', color='w', label='Adult',
#                markerfacecolor='gray', markeredgecolor='black', markersize=12),
#     ]

#     # Add base legend
#     plt.legend(loc='upper right')
#     plt.gca().add_artist(plt.legend(handles=species_legend, title="Species", loc='upper left'))
#     plt.gca().add_artist(plt.legend(handles=age_legend, title="Age Class", loc='lower left'))

#     plt.title(f"Cohort SST Summary: {cohort_tag} ({region_name})")
#     plt.ylabel("SST (°C)")
#     plt.xlabel("Date")
#     plt.grid(True)
#     plt.tight_layout()

#     plot_file = os.path.join(summary_dir, f"{cohort_tag}_{region_name}_summary_plot.png")
#     plt.savefig(plot_file, dpi=150)
#     plt.show()
#     plt.close()

#     print(f"🎯 Summary plot saved → {plot_file}")


# # src/cohort_summary_extractor.py

# import os
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from project_paths import OUTPUTS_DIR

# # CONFIG
# cohort_tag = "2014-12_multi"
# regions = ["Bight_Core", "Transition_Zone", "North_Offshore"]

# for region_name in regions:

#     # Load rolling fingerprint file
#     input_dir = os.path.join(OUTPUTS_DIR, cohort_tag, "cohort_rolling_fingerprint")
#     input_file = os.path.join(input_dir, f"{cohort_tag}_{region_name}_rolling_fingerprint.csv")

#     if not os.path.exists(input_file):
#         print(f"⚠️ Missing rolling fingerprint file for: {region_name} — skipping.")
#         continue

#     df = pd.read_csv(input_file)
#     df['date'] = pd.to_datetime(df['date'])

#     threshold_temp = 14.5

#     mean_sst = df['mean_sst_c'].mean()
#     max_sst = df['mean_sst_c'].max()
#     df['cooling_load'] = np.maximum(0, threshold_temp - df['mean_sst_c'])
#     cdd = df['cooling_load'].sum()
#     sub_thresh_days = (df['mean_sst_c'] < threshold_temp).sum()

#     days_since_start = (df['date'] - df['date'].min()).dt.days
#     slope, intercept = np.polyfit(days_since_start, df['mean_sst_c'], 1)

#     onset_candidates = df[df['mean_sst_c'] < threshold_temp]
#     onset_date = onset_candidates['date'].min() if not onset_candidates.empty else np.nan

#     summary = pd.DataFrame({
#         'cohort_tag': [cohort_tag],
#         'region': [region_name],
#         'mean_sst': [mean_sst],
#         'max_sst': [max_sst],
#         'cdd': [cdd],
#         'sub_threshold_days': [sub_thresh_days],
#         'cooling_slope': [slope],
#         'cooling_onset_date': [onset_date]
#     })

#     summary_dir = os.path.join(OUTPUTS_DIR, cohort_tag, "cohort_summary")
#     os.makedirs(summary_dir, exist_ok=True)
#     summary_file = os.path.join(summary_dir, f"{cohort_tag}_{region_name}_summary.csv")
#     summary.to_csv(summary_file, index=False)
#     print(f"✅ Summary saved → {summary_file}")

#     # Plot
#     plt.figure(figsize=(12, 6))
#     plt.plot(df['date'], df['mean_sst_c'], color='skyblue', label='Daily Mean SST')
#     plt.plot(df['date'], df['rolling_mean'], color='blue', label='5-day Rolling Mean')
#     plt.axhline(mean_sst, color='gray', linestyle='--', label='Window Mean')
#     plt.axhline(threshold_temp, color='red', linestyle=':', label=f'{threshold_temp}°C Threshold')
#     if pd.notnull(onset_date):
#         plt.axvline(onset_date, color='orange', linestyle='--', label='Cooling Onset')

#     plt.title(f"Cohort SST Summary: {cohort_tag} ({region_name})")
#     plt.ylabel("SST (°C)")
#     plt.xlabel("Date")
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()

#     plot_file = os.path.join(summary_dir, f"{cohort_tag}_{region_name}_summary_plot.png")
#     plt.savefig(plot_file, dpi=150)
#     plt.show()
#     plt.close()

#     print(f"🎯 Summary plot saved → {plot_file}")
