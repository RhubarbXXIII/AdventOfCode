Iterable<Iterable<T>> permute<T>(final Iterable<T> items) {
    if (items.length <= 1) {
      return [items];
    }

    return items
      .map((item) => permute(items.where((i) => i != item))
        .map((l) => [item, ...l]).toList())
      .reduce((a, b) => a..addAll(b));
}