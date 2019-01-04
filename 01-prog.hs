
import Data.Set (empty, insert, member)

numbers :: FilePath -> IO [Integer]
numbers =
  fmap mk_numbers . readFile
  where
    mk_numbers :: String -> [Integer]
    mk_numbers = map read . lines . filter (\x -> x /= '+')

first_dup :: [Integer] -> Integer
first_dup ns = head [n | (n, s) <- zip ns seens, member n s]
  where
    seens = scanl (\seen n -> insert n seen) empty ns

main :: IO ()
main =
  do
    ns <- numbers "01-input"
    print $ foldl (+) 0 ns
    print . first_dup . scanl1 (+) . cycle $ ns
