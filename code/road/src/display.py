"""
終端機視覺化顯示

使用 rich 套件在終端機顯示路紙與問路結果
"""

from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns

from .predictor import Predictor


class Display:
    """路紙視覺化顯示器"""

    # 顯示符號
    BANKER_SYMBOL = "●"  # 莊 - 紅色實心
    PLAYER_SYMBOL = "○"  # 閒 - 藍色空心
    RED_SYMBOL = "●"     # 紅 - 衍生路
    BLUE_SYMBOL = "○"    # 藍 - 衍生路
    EMPTY = " "

    def __init__(self, predictor: Predictor):
        self.predictor = predictor
        self.console = Console()

    def _create_big_road_table(self, max_cols: int = 20) -> Table:
        """建立大路表格"""
        table = Table(
            show_header=False,
            show_edge=False,
            pad_edge=False,
            box=None,
            padding=(0, 1),
        )

        # Add columns
        for _ in range(max_cols):
            table.add_column(width=2, justify="center")

        grid = self.predictor.get_big_road().get_grid(max_cols=max_cols)

        for row in grid:
            cells = []
            for cell in row:
                if cell == 'B':
                    cells.append(Text(self.BANKER_SYMBOL, style="bold red"))
                elif cell == 'P':
                    cells.append(Text(self.PLAYER_SYMBOL, style="bold blue"))
                else:
                    cells.append(Text(self.EMPTY))
            table.add_row(*cells)

        return table

    def _create_derived_road_table(
        self,
        results: list[str],
        max_cols: int = 10,
        max_rows: int = 6
    ) -> Table:
        """建立衍生路表格"""
        table = Table(
            show_header=False,
            show_edge=False,
            pad_edge=False,
            box=None,
            padding=(0, 0),
        )

        for _ in range(max_cols):
            table.add_column(width=2, justify="center")

        # Build grid from results (top to bottom, then left to right)
        grid = [[None for _ in range(max_cols)] for _ in range(max_rows)]
        col, row = 0, 0

        for result in results:
            if row >= max_rows:
                col += 1
                row = 0
            if col >= max_cols:
                break
            grid[row][col] = result
            row += 1

        for grid_row in grid:
            cells = []
            for cell in grid_row:
                if cell == 'red':
                    cells.append(Text(self.RED_SYMBOL, style="bold red"))
                elif cell == 'blue':
                    cells.append(Text(self.BLUE_SYMBOL, style="bold blue"))
                else:
                    cells.append(Text(self.EMPTY))
            table.add_row(*cells)

        return table

    def _format_prediction(self, color: Optional[str]) -> Text:
        """格式化預測顏色"""
        if color == 'red':
            return Text("[紅]", style="bold red")
        elif color == 'blue':
            return Text("[藍]", style="bold blue")
        else:
            return Text("[--]", style="dim")

    def show(self) -> None:
        """顯示完整路紙與問路結果"""
        self.console.clear()

        # 大路
        self.console.print(Panel(
            self._create_big_road_table(),
            title="[bold white]大 路[/bold white]",
            border_style="white",
        ))

        # 衍生路 - 並排顯示
        big_eye_table = self._create_derived_road_table(
            self.predictor.get_big_eye_road().results
        )
        small_table = self._create_derived_road_table(
            self.predictor.get_small_road().results
        )
        cockroach_table = self._create_derived_road_table(
            self.predictor.get_cockroach_road().results
        )

        derived_panels = Columns([
            Panel(big_eye_table, title="[bold]大眼仔[/bold]", border_style="white"),
            Panel(small_table, title="[bold]小路[/bold]", border_style="white"),
            Panel(cockroach_table, title="[bold]曱甴路[/bold]", border_style="white"),
        ], equal=True)

        self.console.print(derived_panels)

        # 問路結果
        prediction = self.predictor.ask()

        banker_text = Text()
        banker_text.append("莊問: ", style="bold red")
        banker_text.append("大眼仔")
        banker_text.append_text(self._format_prediction(prediction['if_banker']['big_eye']))
        banker_text.append(" 小路")
        banker_text.append_text(self._format_prediction(prediction['if_banker']['small']))
        banker_text.append(" 曱甴路")
        banker_text.append_text(self._format_prediction(prediction['if_banker']['cockroach']))

        player_text = Text()
        player_text.append("閒問: ", style="bold blue")
        player_text.append("大眼仔")
        player_text.append_text(self._format_prediction(prediction['if_player']['big_eye']))
        player_text.append(" 小路")
        player_text.append_text(self._format_prediction(prediction['if_player']['small']))
        player_text.append(" 曱甴路")
        player_text.append_text(self._format_prediction(prediction['if_player']['cockroach']))

        prediction_panel = Panel(
            Text.assemble(banker_text, "\n", player_text),
            title="[bold white]問 路 結 果[/bold white]",
            border_style="yellow",
        )
        self.console.print(prediction_panel)

    def show_compact(self) -> None:
        """顯示精簡版路紙（只顯示問路結果）"""
        prediction = self.predictor.ask()

        self.console.print("\n[bold]問路結果:[/bold]")

        banker_text = Text()
        banker_text.append("  莊: ", style="bold red")
        for road_name, key in [("大眼仔", 'big_eye'), ("小路", 'small'), ("曱甴路", 'cockroach')]:
            color = prediction['if_banker'][key]
            if color == 'red':
                banker_text.append(f"{road_name}[紅] ", style="red")
            elif color == 'blue':
                banker_text.append(f"{road_name}[藍] ", style="blue")
            else:
                banker_text.append(f"{road_name}[--] ", style="dim")

        player_text = Text()
        player_text.append("  閒: ", style="bold blue")
        for road_name, key in [("大眼仔", 'big_eye'), ("小路", 'small'), ("曱甴路", 'cockroach')]:
            color = prediction['if_player'][key]
            if color == 'red':
                player_text.append(f"{road_name}[紅] ", style="red")
            elif color == 'blue':
                player_text.append(f"{road_name}[藍] ", style="blue")
            else:
                player_text.append(f"{road_name}[--] ", style="dim")

        self.console.print(banker_text)
        self.console.print(player_text)
        self.console.print()
