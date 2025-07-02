# # src/animate_frames.py

# import subprocess
# import os

# # Parameters
# output_tag = "2009-11-multi"
# png_dir = f"png_frames/{output_tag}"

# # Build animation
# subprocess.run(f"""
# ffmpeg -framerate 10 -pattern_type glob -i '{png_dir}/*.png' \
# -vf "scale=iw:ih:force_original_aspect_ratio=decrease,pad=ceil(iw/2)*2:ceil(ih/2)*2" \
# -c:v libx264 -pix_fmt yuv420p {output_tag}_sst_animation.mp4
# """, shell=True)

# print("🎯 Animation complete!")
