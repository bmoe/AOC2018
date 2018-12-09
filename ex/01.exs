fname = "../01-input-test"
fname = "../01-input"

answer1 = File.read!(fname)
|> String.split("\n", trim: true)
|> Enum.map(&String.to_integer(&1))
|> Enum.reduce(0, &(&1 + &2))


IO.puts("Answer One: #{answer1}")


data2 = File.read!(fname) |>
  String.split("\n", trim: true) |>
  Enum.map(&String.to_integer(&1))

process2 = fn (data) ->
  data |>
  Stream.cycle |>
  Stream.scan(0, &(&1 + &2)) |>
  Stream.transform(
    Map.put(Map.new(), 0, 1),
    fn(i, m) ->
      m = Map.update(m, i, 1, &(&1 + 1))
      case Map.get(m, i) >= 2 do
        true -> {[i], m}
        false -> {[nil], m}
      end
    end)
  |>
  Stream.drop_while(&(&1 == nil)) |>
  Stream.take(1) |>
  Enum.to_list |>
  List.first
end

IO.puts("Answer Two: #{process2.(data2)}")

# test0 = process2.([1, -2, 3, 1, 1, -2])  # wants 2
# test1 = process2.([1, -1])               # wants 0
# test2 = process2.([3, 3, 4, -2, -4])     # wants 10
# test3 = process2.([-6, 3, 8, 5, -6])     # wants 5
# test4 = process2.([7, 7, -2, -7, -4])    # wants 14


# IO.puts(inspect test0)
# IO.puts(inspect test1)
# IO.puts(inspect test2)
# IO.puts(inspect test3)
# IO.puts(inspect test4)
