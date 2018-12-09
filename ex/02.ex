defmodule Two do

  def fname do
    "../02-input"
  end

  def data do
    File.read!(fname())
    |> String.split("\n", trim: true)
    |> Enum.map(&String.to_charlist(&1))
  end

  def testdata do
    "abcdef bababc abbcde abcccd aabcdd abcdee ababab"
     |> String.split(~r(\s), trim: true)
     |> Enum.map(&String.trim(&1))
     |> Enum.map(&String.to_charlist(&1))
  end

  def count_letters(s) do
    count_letters(s, Map.new())
  end

  def count_letters([], counts) do
    counts
  end
  def count_letters([x|xs], counts) do
    n = Map.get(counts, x, 0) + 1
    newcounts = Map.put(counts, x, n)
    count_letters(xs, newcounts)
  end

  def countNs(counts, n) do
    counts |>
      Enum.map(&Map.values(&1)) |>
      Enum.map(
        fn x -> Enum.find(x, &(&1 == n)) end
      ) |>
      Enum.filter(&(&1 != nil)) |>
      Kernel.length
  end

  def first(data) do
    counts = Enum.map(data, &count_letters(&1))
    number_of_twos = countNs(counts, 2)
    number_of_threes = countNs(counts, 3)
    IO.puts("#{number_of_twos} * #{number_of_threes} = #{number_of_twos * number_of_threes}")
    number_of_twos * number_of_threes
  end

end

# IO.puts("#{inspect Two.testdata}")
IO.puts("Test Data says: #{Two.first Two.testdata}")
IO.puts("Real Data says: #{Two.first Two.data}")
