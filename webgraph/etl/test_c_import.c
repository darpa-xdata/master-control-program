#include "c_import.h"


void _print_usage()
{
  char* usage = "test_c_import  <graph_type> <graph_name>\n\
    \n\
    graph_format: one of WDC or SNAP\n\
    graph_names: filename to graph (or index_file arc_file for WDC graphs)\n\
\n\
Examples:\n\
    test_c_import SNAP ../data/web-NotreDame.txt\n\
\n\
    test_c_import WDC ../data/pld-arc-sample ../data/pld-index-sample\n\
\n\
Author(s):\n\
    Andy R. Terrel <andy.terrel@gmail.com>\n\
    ";
  printf("%s\n", usage);
}

#include "r_fielder_clustering.hpp"

RInside init_r_env(int argc, char*argv[]) {
  RInside R(argc, argv);
  R.parseEvalQ("source(\"graph_cluster.r\")");
  return R;
}


int main(int argc, char** argv)
{
  if (argc > 4 || argc < 3) {
    _print_usage();
    return 1;
  }

  graph_format_t format = graph_format_from_str(argv[1]);
  char* arc_file = argv[2];
  char* index_file = (argc == 4) ? argv[3] : NULL;
  int max_cluster = atoi(argc[1]);
  graph_t output_graph;
  // ga will be the derived graph with annotation
  derived_graph_and_annotation_t ga;

  load_graph(format, arc_file, index_file, &output_graph);
  ga = td_fielder_cluster(R, g, max_cluster);


  return 0;

}
