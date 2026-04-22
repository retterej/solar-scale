from __future__ import annotations

import typer

from .formatting import format_body
from .service import build_anchor, build_anchor_from_size, scale_from_anchor
from .units import parse_length

app = typer.Typer(help="Solar system scale calculator")


@app.command("calculate")
@app.command(hidden=True)
def calculate(
    object_name: str = typer.Option(..., "--object", help="Anchor object name, e.g. Neptune"),
    value: float = typer.Option(None, "--orbit", help="Anchor distance value"),
    size: float = typer.Option(None, "--size", help="Anchor diameter value"),
    unit: str = typer.Option(..., "--unit", help="Unit for the input value, e.g. ft, m, in"),
) -> None:
    if size is not None:
        parsed = parse_length(size, unit)
        anchor = build_anchor_from_size(object_name, parsed.meters, parsed.original_unit)
    elif value is not None:
        parsed = parse_length(value, unit)
        anchor = build_anchor(object_name, parsed.meters, parsed.original_unit)
    else:
        raise typer.BadParameter("Provide either --orbit or --size")
    scaled = scale_from_anchor(anchor)
    display_rows = [format_body(body, anchor.preferences) for body in scaled]

    typer.echo("")
    typer.echo(
        f"{'Body':<10} {'Orbit (AU)':>10} "
        f"{'Distance':>16} {'Diameter':>16}"
    )
    typer.echo("-" * 58)

    for row in display_rows:
        orbit = f"{row.orbit_au:.3f}" if row.orbit_au >= 0.0005 else "--"
        typer.echo(
            f"{row.name:<10} "
            f"{orbit:>10} "
            f"{row.distance_display:>16} "
            f"{row.diameter_display:>16}"
        )


if __name__ == "__main__":
    app()