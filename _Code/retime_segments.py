import subprocess
import os
import sys

def main():
    audio_bounds = [
        (0.00, 0.95), (0.95, 8.30), (8.30, 13.80), (13.80, 20.05), (20.05, 23.32),
        (23.32, 28.28), (28.28, 34.24), (34.24, 36.84), (36.84, 42.82), (42.82, 49.61),
        (49.61, 55.63), (55.63, 59.81), (59.81, 62.19), (62.19, 65.93), (65.93, 71.01),
        (71.01, 74.82), (74.82, 77.76), (77.76, 80.98), (80.98, 85.21), (85.21, 89.02),
        (89.02, 92.17), (92.17, 93.59), (93.59, 97.17), (97.17, 101.06), (101.06, 106.51),
        (106.51, 110.86), (110.86, 116.54), (116.54, 124.73), (124.73, 127.22), (127.22, 129.92),
        (129.92, 132.92), (132.92, 137.52), (137.52, 144.50), (144.50, 147.11), (147.11, 153.53),
        (153.53, 154.76), (154.76, 160.89), (160.89, 166.99), (166.99, 171.10), (171.10, 174.32),
        (174.32, 180.17), (180.17, 184.29), (184.29, 186.68), (186.68, 194.71), (194.71, 202.12),
        (202.12, 205.48), (205.48, 209.08), (209.08, 214.43), (214.43, 218.87), (218.87, 222.63),
        (222.63, 232.97), (232.97, 241.44), (241.44, 244.82), (244.82, 249.53), (249.53, 255.36),
        (255.36, 261.04), (261.04, 272.37), (272.37, 276.15), (276.15, 277.60)
    ]

    v_trans = [
        2.80, 4.40, 11.87, 17.07, 23.40, 27.27, 31.93, 37.40, 40.20, 45.93,
        51.73, 58.33, 63.27, 65.73, 69.33, 74.80, 78.67, 82.00, 85.53, 89.93,
        93.80, 97.40, 99.87, 103.13, 107.00, 112.47, 117.47, 122.93, 130.40, 133.40,
        136.67, 140.00, 144.93, 152.67, 155.67, 160.60, 162.80, 169.13, 174.40, 178.47,
        182.33, 188.40, 192.80, 195.53, 202.40, 209.27, 212.60, 216.13, 221.40, 225.53,
        229.33, 237.07, 243.13, 246.40, 250.80, 256.33, 261.53, 271.73, 275.87, 278.00
    ]

    cum_frames = [round(b[1] * 15) for b in audio_bounds]
    start_frames = [0] + cum_frames[:-1]
    frame_counts = [cum_frames[i] - start_frames[i] for i in range(len(audio_bounds))]

    out_dir = '/tmp/sync_segs'
    os.makedirs(out_dir, exist_ok=True)

    concat_lines = []
    print(f'Starting exact frame retiming of {len(audio_bounds)} segments (total frames: {sum(frame_counts)})...')

    for i in range(len(audio_bounds)):
        vs = v_trans[i]
        ve = v_trans[i+1]
        vdur = ve - vs
        n_frames = frame_counts[i]
        adur = n_frames / 15.0
        factor = adur / vdur
        seg_file = os.path.join(out_dir, f'seg_{i:02d}.mp4')
        
        cmd = [
            'ffmpeg', '-y',
            '-ss', f'{vs:.3f}', '-t', f'{vdur:.3f}',
            '-i', 'derivatives_video.mp4',
            '-vf', f'setpts={factor:.6f}*PTS,fps=15',
            '-vframes', str(n_frames),
            '-an',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
            seg_file
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode != 0:
            print(f'Error processing segment {i}: return code {res.returncode}', file=sys.stderr)
            sys.exit(1)
        
        concat_lines.append(f"file '{seg_file}'")
        if (i + 1) % 10 == 0 or (i + 1) == len(audio_bounds):
            print(f'Processed {i+1}/{len(audio_bounds)} segments')

    concat_file = os.path.join(out_dir, 'concat.txt')
    with open(concat_file, 'w') as f:
        f.write('\n'.join(concat_lines) + '\n')
    print(f'Wrote concat list to {concat_file}')

if __name__ == '__main__':
    main()
