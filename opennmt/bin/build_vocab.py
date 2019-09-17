"""Standalone script to generate word vocabularies from monolingual corpus."""

import argparse

from opennmt import constants
from opennmt import tokenizers
from opennmt import utils


def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      "data", nargs="*",
      help="Source text file.")
  parser.add_argument(
      "--from_vocab", default=None,
      help="Build from a saved vocabulary (see also --from_format).")
  parser.add_argument(
      "--from_format", default="default", choices=["default", "sentencepiece"],
      help="The format of the saved vocabulary (see also --from_vocab).")
  parser.add_argument(
      "--save_vocab", required=True,
      help="Output vocabulary file.")
  parser.add_argument(
      "--min_frequency", type=int, default=1,
      help="Minimum word frequency.")
  parser.add_argument(
      "--size", type=int, default=0,
      help="Maximum vocabulary size. If = 0, do not limit vocabulary.")
  parser.add_argument(
      "--size_multiple", type=int, default=1,
      help=("Ensure that the vocabulary size + 1 is a multiple of this value "
            "(+ 1 represents the <unk> token that will be added during the training."))
  parser.add_argument(
      "--without_sequence_tokens", default=False, action="store_true",
      help="If set, do not add special sequence tokens (start, end) in the vocabulary.")
  tokenizers.add_command_line_arguments(parser)
  args = parser.parse_args()

  tokenizer = tokenizers.build_tokenizer(args)

  special_tokens = [constants.PADDING_TOKEN]
  if not args.without_sequence_tokens:
    special_tokens.append(constants.START_OF_SENTENCE_TOKEN)
    special_tokens.append(constants.END_OF_SENTENCE_TOKEN)

  vocab = utils.Vocab(
      special_tokens=special_tokens,
      from_file=args.from_vocab,
      from_format=args.from_format)
  for data_file in args.data:
    vocab.add_from_text(data_file, tokenizer=tokenizer)
  vocab = vocab.prune(max_size=args.size, min_frequency=args.min_frequency)
  vocab.pad_to_multiple(args.size_multiple, num_oov_buckets=1)
  vocab.serialize(args.save_vocab)


if __name__ == "__main__":
  main()
