
# FUCK NO
# This stupid deque implementation, Dlist, has no way to remove elements. WTF?

defmodule Nine do
  alias Dlist.DoublyLinkedList, as: D

  @moduledoc """
  Documentation for Nine.
  """

  @doc """
  Hello world.

  ## Examples

      iex> Nine.hello
      :world

  """
  def hello do
    :world
  end

  def empty_circle do
    {:ok, circle} = D.new
    D.append(circle, 0)
    circle
  end

  def ccw(circle, n) do
    # d.append(d.popleft())   rotate left
    cond do
      n > 0 ->
        D.append(circle, D.first(circle))
        ccw(circle, n-1)
      n == 0 ->
        circle
      n < 0 ->
        ccw(circle, 0-n)
    end
  end

  def cw(circle, n) do
    # d.appendleft(d.pop())   rotate right
    cond do
      n > 0 ->
        D.prepend(circle, D.last(circle))
        cw(circle, n-1)
      n == 0 ->
        circle
      n < 0 ->
        cw(circle, 0-n)
    end
  end

  def new_board(nelves) do
    { empty_circle(), Map.new(), nelves, 1 }
  end

  def step ({circle, scores, nplayers, next_marble}) do
    case rem(next_marble, 23) == 0 do
      false ->
        # place marble into the circle between the marbles that are 1 and 2
        # marbles clockwise of the current marble
        circle = cw(circle, 1)
        D.prepend(circle, next_marble)  # mutation. gross.
        {circle, scores, nplayers, next_marble + 1}
      true -> :undefined
    end
  end

end
