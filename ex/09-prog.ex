
defmodule Circle do
  # current: {index, marblenumber}
  defstruct marbles: [0], current: {0, 0}, mod: 1

  def debug do
    false
  end


  def new do
    %Circle{}
  end

  def clockwise(%Circle{marbles: marbles, current: {currpos, _}, mod: mod}, n) do
    pos = rem(currpos + n, mod)
    {pos, Enum.at(marbles, pos)}
  end

  def counterclockwise(circle = %Circle{mod: mod}, n) do
    clockwise(circle, mod - n)
  end

  def addmarble(circle = %Circle{marbles: marbles, mod: mod}, marblenumber) do
    {nextpos, _} = clockwise(circle, 2)
    new_marbles = List.insert_at(marbles, nextpos, marblenumber)
    %{circle | current: {nextpos, marblenumber}, marbles: new_marbles, mod: mod+1}
  end

  def rule23(circle = %Circle{marbles: marbles, mod: mod}) do
    # Get special marble
    {xpos, xval} = counterclockwise(circle, 7)
    newmarbles = List.delete_at(marbles, xpos)
    newmod = mod - 1
    newpos = rem(xpos, newmod)
    newcurrent = {newpos, Enum.at(newmarbles, newpos)}
    newcircle = %{circle | marbles: newmarbles, mod: newmod, current: newcurrent}
    {xval, newcircle}
  end

  def show_marble({marblenumber, index}, special_index) do
    tag = if special_index == index do "*" else " " end
    String.pad_leading(" #{tag}#{marblenumber}", 3)
  end
  def show(%Circle{marbles: marbles, current: {cpos, _}}) do
    Enum.with_index(marbles)
    |> Enum.map(&show_marble(&1, cpos))
    |> Enum.join
  end

  def step({circle, scoreboard = {num_elves, scores}, marblenumber}) do
    case rem(marblenumber, 23) do
      0 ->
        {removed_marble, newcircle} = rule23(circle)
        points = removed_marble + marblenumber
        elfnumber = rem(marblenumber, num_elves)
        newscores = Map.update(scores, elfnumber, points, &(&1 + points))
        if debug() do IO.puts(show(newcircle)) end
        {newcircle, {num_elves, newscores}, marblenumber + 1}
      _ ->
        newcircle = addmarble(circle, marblenumber)
        if debug() do IO.puts(show(newcircle)) end
        {newcircle, scoreboard, marblenumber + 1}
    end
  end


end

defmodule Nine do
  def run_first(num_elves, last_step) do
    scoreboard = {num_elves, Map.new()}
    Stream.iterate({Circle.new, scoreboard, 1}, &Circle.step/1)
    |> Stream.drop(last_step) # ignore intermediate boards
    |> Stream.take(1)  # Pop off final boad
    |> Enum.to_list # listify
    |> List.first   # final board, delistified
    |> fn({_circle, {_num_elves, scores}, _nextmarble}) ->
      scores
      |> Map.values
      |> Enum.max
    end.()
  end

  def test do
    tests = [
      {9, 25, 32},
      {10, 1618, 8317}, {13, 7999, 146373},
      {17, 1104, 2764}, {21, 6111, 54718}, {30, 5807, 37305}
    ]
    tests
    |> Stream.map(
    fn({elves, marbles, expected_score}) ->
      actual_score = run_first(elves, marbles)
      case actual_score == expected_score do
        true ->
          "PASSED #{actual_score} == #{expected_score}"
        false ->
          "FAILED #{actual_score} != #{expected_score}"
      end
    end
    )
    |> Stream.map(&IO.puts/1)
    |> Stream.run
    :ok
  end

  def first do
    start = Time.utc_now()
    IO.puts("Started at #{start}")
    answer = run_first(403, 71920)
    stopped = Time.utc_now()
    IO.puts("Stopped at #{stopped}")
    IO.puts("It took #{Time.diff(stopped, start)} seconds")
    answer
  end

  def second do
    start = Time.utc_now()
    IO.puts("Started at #{start}")
    answer = run_first(403, 7192000)
    stopped = Time.utc_now()
    IO.puts("Stopped at #{stopped}")
    IO.puts("It took #{Time.diff(stopped, start)} seconds")
    answer
  end
end
