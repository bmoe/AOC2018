
import Data.Map (empty, insert, lookup, Map, elems)
import Data.Set (fromList, member)

testData :: [String]
testData = lines "abcdef\nbababc\nabbcde\nabcccd\naabcdd\nabcdee\nababab"

counts :: String -> Map Char Integer
counts code =
  foldl count empty code
  where
    count :: Map Char Integer -> Char -> Map Char Integer
    count m ch = insert ch (n+1) m
      where
        n = case (Data.Map.lookup ch m) of
          Nothing -> 0
          Just c -> c

first :: [String] -> Int
first codes =
  length threes * length twos
  where
    counted = map counts codes
    twos = ['x' | c <- map fromList (map elems counted), 2 `member` c]
    threes = ['x' | c <- map fromList (map elems counted), 3 `member` c]


diffByOne _ [] = False
diffByOne [] _ = False
diffByOne (x:ys) (y:xs)
  | x /= y = xs == ys
  | otherwise = diffByOne xs ys

secondPuzzle codes =
  [a | (a, b) <- zip correctA correctB, a == b]
  where
    (correctA, correctB) = head [(a, b) | a <- codes, b <- codes, diffByOne a b]

main :: IO ()
main = do
  d <- readFile "02-input"
  putStr "Test First Result: "
  print . first $ testData
  putStr "Real First Result: "
  print . first $ lines d
  putStr "Second - correct codes: "
  print . head $ [(a, b) | a <- lines d, b <- lines d, diffByOne a b]
  putStr "Second - common characters: "
  print . secondPuzzle $ lines d
