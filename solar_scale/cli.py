import typer
from .service import scale_system

app = typer.Typer(add_completion=False)


@app.command("calculate")
@app.command(hidden=True)
def calculate(neptune_distance_ft: float = typer.Option(..., help="Neptune's distance in feet")):
    results = scale_system(neptune_distance_ft)

    typer.echo("")
    typer.echo(f"{'Body':<10} {'AU':>6} {'Distance(ft)':>15} {'Diameter(in)':>15}")
    typer.echo("-" * 52)

    for r in results:
        typer.echo(
            f"{r['name']:<10} "
            f"{r['au']:>6.3f} "
            f"{r['distance_ft']:>15.2f} "
            f"{r['diameter_in']:>15.4f}"
        )
