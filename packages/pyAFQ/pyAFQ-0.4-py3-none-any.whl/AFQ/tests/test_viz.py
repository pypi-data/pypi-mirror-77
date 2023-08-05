import pytest

from AFQ.viz.utils import Viz


def test_viz_name_errors():
    Viz("fury")

    with pytest.raises(
        TypeError,
        match="Visualization backend should be"
        + " either 'plotly' or 'fury'. "
            + "It is currently set to plotlyy"):
        Viz("plotlyy")
