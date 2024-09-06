import Levenshtein as lev
import networkx as nx
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def read_barcodes_from_merged(file_path, word1, word2, start_text, end_text):
    barcodes = []
    with open(file_path, 'r') as merged:
        for line in merged:
            if word1 in line and word2 in line:
                start_index = line.find(start_text) + len(start_text)
                end_index = line.find(end_text, start_index)
                if start_index != -1 and end_index != -1:
                    word3 = line[start_index:end_index]
                    barcodes.append(word3)
    return barcodes


def replace_long_sequences(barcodes, length_threshold):
    short_sequences = [barcode for barcode in barcodes if len(barcode) <= length_threshold]
    long_sequences = [barcode for barcode in barcodes if len(barcode) > length_threshold]
    replaced_sequences = []
    for long_seq in long_sequences:
        replaced = False
        for short_seq in short_sequences:
            if short_seq in long_seq:
                replaced_sequences.append(short_seq)
                replaced = True
                break
        if not replaced:
            replaced_sequences.append(long_seq)
    return short_sequences + replaced_sequences


def cluster_barcodes(barcodes, distance_threshold):
    G = nx.Graph()
    for barcode in barcodes:
        G.add_node(barcode)
    for i, barcode1 in enumerate(barcodes):
        for j in range(i + 1, len(barcodes)):
            barcode2 = barcodes[j]
            if lev.distance(barcode1, barcode2) <= distance_threshold:
                G.add_edge(barcode1, barcode2)
    clusters = list(nx.connected_components(G))
    return clusters


def most_common_barcodes(cluster, n=3):
    return Counter(cluster).most_common(n)


def reprint_with_common_barcodes(original_barcodes, clusters):
    barcode_to_cluster = {}
    cluster_list = []
    for cluster in clusters:
        for barcode in cluster:
            barcode_to_cluster[barcode] = cluster
    for original_barcode in original_barcodes:
        if original_barcode in barcode_to_cluster:
            cluster_list.append((barcode_to_cluster[original_barcode], original_barcode))
        else:
            cluster_list.append((set(), original_barcode))
    return cluster_list


def analyze_barcodes(barcodes, top_n=3):
    line_counts = Counter(barcodes)
    most_common_lines = line_counts.most_common(top_n)
    total_lines = len(barcodes)
    most_common_percentages = [(line, (count / total_lines) * 100) for line, count in most_common_lines]
    return most_common_percentages


def process_barcodes(merged_file_path, word1, word2, start_text, end_text, length_threshold, distance_threshold):
    barcodes = read_barcodes_from_merged(merged_file_path, word1, word2, start_text, end_text)
    barcodes = replace_long_sequences(barcodes, length_threshold)
    clusters = cluster_barcodes(barcodes, distance_threshold)
    clustered_barcodes = reprint_with_common_barcodes(barcodes, clusters)

    cluster_dict = defaultdict(list)
    for cluster, barcode in clustered_barcodes:
        cluster_dict[frozenset(cluster)].append(barcode)

    all_common_barcodes = []
    for cluster, barcodes_in_cluster in cluster_dict.items():
        most_common_barcodes_list = most_common_barcodes(barcodes_in_cluster, 1)
        most_common = most_common_barcodes_list[0][0]
        for _ in barcodes_in_cluster:
            modified_barcode = f"G{most_common}"
            all_common_barcodes.append(modified_barcode)

    return analyze_barcodes(all_common_barcodes, top_n=3)


def process_all_pairs(output_summary_path, output_pdf_path, text_filename, start_text, end_text, length_threshold,
                      distance_threshold, rows, columns):
    array_2d = [[(rows[i], columns[j]) for j in range(len(columns))] for i in range(len(rows))]
    processed_pairs = 0
    output = ""

    with PdfPages(output_pdf_path) as pdf:
        for row_idx in range(len(array_2d)):
            for col_idx in range(len(array_2d[row_idx])):
                word1, word2 = array_2d[row_idx][col_idx]
                most_common_percentages_after = process_barcodes(text_filename, word1, word2, start_text, end_text,
                                                                 length_threshold, distance_threshold)
                output += f"R{row_idx + 1}C{col_idx + 1}: {', '.join([f'{line} ({percentage:.2f}%)' for line, percentage in most_common_percentages_after])}\n"

                fig, ax = plt.subplots(figsize=(10, 6))
                labels, percentages = zip(*most_common_percentages_after)
                ax.bar(labels, percentages, color='blue')
                ax.set_title(f'R{row_idx + 1}C{col_idx + 1}: {word1} - {word2}')
                ax.set_xlabel('Barcode')
                ax.set_ylabel('Percentage')
                ax.set_ylim(0, 100)
                ax.tick_params(axis='x', labelsize=8)

                pdf.savefig(fig)
                plt.close(fig)

                processed_pairs += 1
                if processed_pairs >= 96:
                    break
            if processed_pairs >= 96:
                break

    with open(output_summary_path, 'w') as summary_file:
        summary_file.write(output)
