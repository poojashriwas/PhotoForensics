def hamming_distance(hash1, hash2):
    return hash1 - hash2


def match_hashes(blocks, max_distance=6):

    matches = []

    total = len(blocks)

    for i in range(total):

        hash1 = blocks[i]["hash"]

        for j in range(i + 1, total):

            hash2 = blocks[j]["hash"]

            distance = hamming_distance(hash1, hash2)

            if distance <= max_distance:

                matches.append(
                    (
                        blocks[i],
                        blocks[j],
                        distance
                    )
                )

    return matches