#!/usr/bin/env python3
"""Fluid type and space scales as CSS clamp() custom properties.

Each step grows smoothly between a phone width and a desktop width instead of jumping
at breakpoints (the Utopia method). Sizes are in rem so browser text zoom still works.

  scale.py type  [--min-base 16] [--max-base 18] [--min-ratio 1.2] [--max-ratio 1.333]
                 [--steps-up 6] [--steps-down 2] [--min-width 360] [--max-width 1280]
  scale.py space [--min-base 16] [--max-base 18] [--min-width 360] [--max-width 1280]

Ratios: 1.125 dense app, 1.2 product UI, 1.25 general web, 1.333 marketing/editorial,
1.5+ dramatic display. Give the phone a smaller ratio than the desktop.
"""
import argparse

ROOT_PX = 16
SPACE_MULTIPLIERS = [("3xs", 0.25), ("2xs", 0.5), ("xs", 0.75), ("s", 1), ("m", 1.5),
                     ("l", 2), ("xl", 3), ("2xl", 4), ("3xl", 6), ("4xl", 8)]


def clamp(min_px, max_px, min_width, max_width):
    """CSS clamp() that is min_px at min_width and max_px at max_width."""
    if abs(max_px - min_px) < 0.01:
        return f"{min_px / ROOT_PX:.4f}rem"
    slope = (max_px - min_px) / (max_width - min_width)
    intercept_rem = (min_px - slope * min_width) / ROOT_PX
    low, high = sorted((min_px, max_px))
    return f"clamp({low / ROOT_PX:.4f}rem, {intercept_rem:.4f}rem + {slope * 100:.4f}vw, {high / ROOT_PX:.4f}rem)"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("kind", choices=["type", "space"])
    parser.add_argument("--min-base", type=float, default=16)
    parser.add_argument("--max-base", type=float, default=18)
    parser.add_argument("--min-ratio", type=float, default=1.2)
    parser.add_argument("--max-ratio", type=float, default=1.333)
    parser.add_argument("--steps-up", type=int, default=6)
    parser.add_argument("--steps-down", type=int, default=2)
    parser.add_argument("--min-width", type=float, default=360)
    parser.add_argument("--max-width", type=float, default=1280)
    args = parser.parse_args()

    lines = [":root {"]
    if args.kind == "type":
        for step in range(-args.steps_down, args.steps_up + 1):
            # Below the base size both ends use the smaller ratio; otherwise the larger desktop
            # ratio would make small text *shrink* as the screen grows.
            max_ratio = args.max_ratio if step >= 0 else args.min_ratio
            small = args.min_base * args.min_ratio ** step
            large = args.max_base * max_ratio ** step
            lines.append(f"  --step-{step}: {clamp(small, large, args.min_width, args.max_width)}; "
                         f"/* {small:.1f}px -> {large:.1f}px */")
    else:
        for name, multiplier in SPACE_MULTIPLIERS:
            small, large = args.min_base * multiplier, args.max_base * multiplier
            lines.append(f"  --space-{name}: {clamp(small, large, args.min_width, args.max_width)}; "
                         f"/* {small:.0f}px -> {large:.0f}px */")
    lines.append("}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
