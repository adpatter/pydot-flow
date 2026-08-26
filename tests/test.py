import pydot

from pydot_flow import Chart


def test_create_node_adds_node_to_chart():
    chart = Chart(rankdir="TB")

    node = chart.create_node(src_node_attrs={"label": "Node 1"})

    assert node.get_graph() is chart.get_graph()
    assert any(
        candidate.get_name() == node.get_name()
        for candidate in chart.get_graph().get_node_list()
    )
    assert node.get_pydot_node().get_label() == "Node 1"


def test_flow_adds_node_and_edge():
    chart = Chart()
    source = chart.create_node(src_node_attrs={"label": "Source"})

    destination = source.flow(
        src_port="s",
        dst_node_attrs={"name": "destination"},
        edge_attrs={"label": "source-destination"},
    )

    assert destination.get_name() == "destination"
    assert len(chart.get_graph().get_node_list()) == 2
    assert len(chart.get_graph().get_edge_list()) == 1
    edge = chart.get_graph().get_edge_list()[0]
    assert edge.get_label() == "source-destination"


def test_flow_can_reuse_an_existing_node():
    chart = Chart()
    source = chart.create_node(src_node_attrs={"label": "Source"})
    destination = source.flow(
        src_port="s", dst_node_attrs={"label": "Destination"}
    )

    reused = source.flow(src_port="e", dst_node_attrs={"name": destination.get_name()})

    assert reused.get_name() == destination.get_name()
    assert len(chart.get_graph().get_node_list()) == 2
    assert len(chart.get_graph().get_edge_list()) == 2


def test_flow_can_add_an_edge_to_a_subgraph():
    chart = Chart()
    source = chart.create_node(src_node_attrs={"label": "Source"})
    subgraph = pydot.Subgraph(rank="same")

    destination = source.flow(
        src_port="e",
        dst_node_attrs={"name": "destination"},
        graph=subgraph,
    )

    assert destination.get_graph() is subgraph
    assert any(
        candidate.get_name() == subgraph.get_name()
        for candidate in chart.get_graph().get_subgraph_list()
    )
    assert len(subgraph.get_edge_list()) == 1
