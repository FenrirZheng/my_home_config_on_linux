#!/usr/bin/env python3
"""
百家樂大問路系統

使用方式:
    python main.py                    # 互動模式
    python main.py "BPBPPBBB"         # 直接輸入結果字串
    python main.py --compact "BPBPPBBB"  # 精簡輸出模式
"""

import sys
from src.predictor import Predictor
from src.display import Display


def main():
    predictor = Predictor()
    display = Display(predictor)

    # Check command line arguments
    compact_mode = '--compact' in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]

    if args:
        # Direct input mode
        results = args[0].upper()
        predictor.add_results(results)

        if compact_mode:
            display.show_compact()
        else:
            display.show()
    else:
        # Interactive mode
        print("百家樂大問路系統")
        print("=" * 40)
        print("輸入: B=莊, P=閒, Q=離開")
        print("=" * 40)

        while True:
            try:
                user_input = input("\n輸入結果 (B/P/Q): ").strip().upper()

                if user_input == 'Q':
                    print("再見!")
                    break

                if not user_input:
                    continue

                # Add results
                for char in user_input:
                    if char in ('B', 'P'):
                        predictor.add_result(char)

                # Show updated display
                display.show()

            except KeyboardInterrupt:
                print("\n再見!")
                break
            except EOFError:
                break


if __name__ == "__main__":
    main()
