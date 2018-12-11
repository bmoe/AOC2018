defmodule NineTest do
  use ExUnit.Case
  doctest Nine

  test "greets the world" do
    assert Nine.hello() == :world
  end
end
