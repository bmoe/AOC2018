defmodule Eight do

  def data() do
    File.read!("../08-input")
    |> String.trim
    |> String.split(~r( ), trim: true)
    |> Enum.map(&String.to_integer/1)
  end

  def test_data() do
    "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    |> String.split(~r( ))
    |> Enum.map(&String.to_integer/1)
  end

  def parse_nodes(inp, 0) do
    {[], inp}
  end
  def parse_nodes([], _) do
    {[], :error}
  end
  def parse_nodes(inp, 1) do
    {node, rest} = parse_node(inp)
    {[node], rest}
  end
  def parse_nodes(inp, n) do
    {node, rest_one} = parse_node(inp)
    {nodes, rest} = parse_nodes(rest_one, n-1)
    {[node|nodes], rest}
  end

  def parse_node([nkids, nmetas | input]) do
    {kids, rest_one} = parse_nodes(input, nkids)
    {meta, rest} = Enum.split(rest_one, nmetas)
    {{kids, meta}, rest}
  end

  # Sum up the metadata for first part
  def process([]) do
    0
  end
  def process(nodes) do
    Enum.reduce(
      nodes,
      0,
      fn({kids, meta}, acc) ->
        acc + Enum.sum(meta) + process(kids)
    end)
  end

  def first_test do
    {n, []} = parse_node(test_data())
    process [n]
  end

  def first do
    {n, []} = parse_node(data())
    process [n]
  end

  # Sum up the metadata for second part
  def process2({[], meta}) do
    Enum.sum meta
  end
  def process2({kids, meta}) do
    kidvals = Enum.map(kids, &process2/1)
    Enum.reduce(
      meta,
      0,
      fn (i, acc) ->
        # IO.puts("My i: #{i}")
        # IO.puts("MY KIDVALS: #{inspect kidvals, charlists: :as_lists}")
        next = if i == 0 do
          acc
        else
          acc + Enum.at(kidvals, i-1, 0)
        end
      end
    )
  end

  def second_test do
    {n, []} = parse_node(test_data())
    process2(n)
  end

  def second do
    {n, []} = parse_node(data())
    process2(n)
  end

end

IO.puts("First test: #{inspect Eight.first_test()}")
IO.puts("First real: #{inspect Eight.first()}")
IO.puts("")
IO.puts("Second test: #{inspect Eight.second_test()}")
IO.puts("Second real: #{inspect Eight.second()}")

# First test: 138
# First real: 36627
#
# Second test: 66
# Second real: 16695


#  2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
#  A----------------------------------
#      B----------- C-----------
#                       D-----

# {n, []} = Eight.parse_node Eight.test_data
