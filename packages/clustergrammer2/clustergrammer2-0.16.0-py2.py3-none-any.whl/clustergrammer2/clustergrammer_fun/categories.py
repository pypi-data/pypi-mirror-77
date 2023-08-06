def check_categories(lines):
  '''
  find out how many row and col categories are available
  when loading data from file
  '''
  # count the number of row categories
  rcat_line = lines[0].split('\t')

  # calc the number of row names and categories
  num_rc = 0
  found_end = False

  # skip first tab
  for inst_string in rcat_line[1:]:
    if inst_string == '':
      if found_end is False:
        num_rc = num_rc + 1
    else:
      found_end = True

  max_rcat = 15
  if max_rcat > len(lines):
    max_rcat = len(lines) - 1

  num_cc = 0
  for i in range(max_rcat):
    ccat_line = lines[i + 1].split('\t')

    # make sure that line has length greater than one to prevent false cats from
    # trailing new lines at end of matrix
    if ccat_line[0] == '' and len(ccat_line) > 1:
      num_cc = num_cc + 1

  num_labels = {}
  num_labels['row'] = num_rc + 1
  num_labels['col'] = num_cc + 1

  return num_labels

def dict_cat(net, define_cat_colors=False):
  '''
  make a dictionary of node-category associations
  '''
  net.persistent_cat_colors = True

  for inst_rc in ['row', 'col']:
    inst_keys = list(net.dat['node_info'][inst_rc].keys())
    all_cats = [x for x in inst_keys if 'cat-' in x]

    for inst_name_cat in all_cats:

      dict_cat = {}
      tmp_cats = net.dat['node_info'][inst_rc][inst_name_cat]
      tmp_nodes = net.dat['nodes'][inst_rc]

      for i in range(len(tmp_cats)):
        inst_cat = tmp_cats[i]
        inst_node = tmp_nodes[i]

        if inst_cat not in dict_cat:
          dict_cat[inst_cat] = []

        dict_cat[inst_cat].append(inst_node)

      tmp_name = 'dict_' + inst_name_cat.replace('-', '_')
      net.dat['node_info'][inst_rc][tmp_name] = dict_cat

  # merge with old cat_colors by default
  cat_colors = net.viz['cat_colors']

  if define_cat_colors == True:
    cat_number = 0

    for inst_rc in ['row', 'col']:

      inst_keys = list(net.dat['node_info'][inst_rc].keys())
      all_cats = [x for x in inst_keys if 'cat-' in x]

      for cat_index in all_cats:

        if cat_index not in cat_colors[inst_rc]:
          cat_colors[inst_rc][cat_index] = {}

        cat_names = sorted(list(set(net.dat['node_info'][inst_rc][cat_index])))

        # loop through each category name and assign a color
        for tmp_name in cat_names:

          # using the same rules as the front-end to define cat_colors
          inst_color = get_cat_color(cat_number + cat_names.index(tmp_name))

          check_name = tmp_name

          # check if category is string type and non-numeric
          try:
            float(check_name)
            is_string_cat = False
          except:
            is_string_cat = True

          if is_string_cat == True:
            # check for default non-color
            if ': ' in check_name:
              check_name = check_name.split(': ')[1]

            # if check_name == 'False' or check_name == 'false':
            if 'False' in check_name or 'false' in check_name:
              inst_color = '#eee'

            if 'Not ' in check_name:
              inst_color = '#eee'

          # do not overwrite old colors
          if tmp_name not in cat_colors[inst_rc][cat_index] and is_string_cat:

            cat_colors[inst_rc][cat_index][tmp_name] = inst_color
            # print('overwrite: ' + tmp_name + ' -> ' + str(inst_color))

          cat_number = cat_number + 1

    net.viz['cat_colors'] = cat_colors

    net.viz['global_cat_colors'] = {}

    global_cat_colors = {}
    for axis in net.viz['cat_colors']:
        for cat_index in net.viz['cat_colors'][axis]:

            inst_dict = net.viz['cat_colors'][axis][cat_index]

            for inst_full_name in inst_dict:

                inst_name = inst_full_name.split(': ')[1]
                inst_color = inst_dict[inst_full_name]

                global_cat_colors[inst_name] = inst_color

    net.viz['global_cat_colors'] = global_cat_colors


def calc_cat_clust_order(net, inst_rc):
  '''
  cluster category subset of data
  '''
  from .__init__ import Network
  from copy import deepcopy
  from . import calc_clust, run_filter

  inst_keys = list(net.dat['node_info'][inst_rc].keys())
  all_cats = [x for x in inst_keys if 'cat-' in x]

  if len(all_cats) > 0:

    for inst_name_cat in all_cats:

      tmp_name = 'dict_' + inst_name_cat.replace('-', '_')
      dict_cat = net.dat['node_info'][inst_rc][tmp_name]

      unordered_cats = dict_cat.keys()

      ordered_cats = order_categories(unordered_cats)

      # this is the ordering of the columns based on their category, not
      # including their clustering ordering within category
      all_cat_orders = []
      tmp_names_list = []
      for inst_cat in ordered_cats:

        inst_nodes = dict_cat[inst_cat]

        tmp_names_list.extend(inst_nodes)

      names_clust_list = tmp_names_list

      # calc category-cluster order
      final_order = []

      for i in range(len(net.dat['nodes'][inst_rc])):

        inst_node_name = net.dat['nodes'][inst_rc][i]
        inst_node_num = names_clust_list.index(inst_node_name)

        final_order.append(inst_node_num)

      inst_index_cat = inst_name_cat.replace('-', '_') + '_index'

      net.dat['node_info'][inst_rc][inst_index_cat] = final_order


def order_categories(unordered_cats):
  '''
  If categories are strings, then simple ordering is fine.
  If categories are values then I'll need to order based on their values.
  The final ordering is given as the original categories (including titles) in a
  ordered list.
  '''

  no_titles = remove_titles(unordered_cats)

  all_are_numbers = check_all_numbers(no_titles)

  if all_are_numbers:
    ordered_cats = order_cats_based_on_values(unordered_cats, no_titles)
  else:
    ordered_cats = sorted(unordered_cats)

  return ordered_cats


def order_cats_based_on_values(unordered_cats, values_list):
  import pandas as pd

  try:
    # convert values_list to values
    values_list = [float(i) for i in values_list]

    inst_series = pd.Series(data=values_list, index=unordered_cats)

    inst_series.sort_values(inplace=True)

    ordered_cats = inst_series.index.tolist()

    # ordered_cats = unordered_cats
  except:
    # keep default ordering if error occurs
    print('error sorting cats based on values ')
    ordered_cats = unordered_cats

  return ordered_cats

def check_all_numbers(no_titles):
  all_numbers = True
  for tmp in no_titles:
    if is_number(tmp) == False:
      all_numbers = False

  return all_numbers

def remove_titles(cats):
  from copy import deepcopy

  # check if all have titles
  ###########################
  all_have_titles = True

  for inst_cat in cats:
    if is_number(inst_cat) == False:
      if ': ' not in inst_cat:
        all_have_titles = False
    else:
      all_have_titles = False

  if all_have_titles:
    no_titles = cats
    no_titles = [i.split(': ')[1] for i in no_titles]

  else:
    no_titles = cats

  return no_titles

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_cat_color(cat_num):

  all_colors = [ "#393b79", "#aec7e8", "#ff7f0e", "#ffbb78", "#98df8a", "#bcbd22",
    "#404040", "#ff9896", "#c5b0d5", "#8c564b", "#1f77b4", "#5254a3", "#FFDB58",
    "#c49c94", "#e377c2", "#7f7f7f", "#2ca02c", "#9467bd", "#dbdb8d", "#17becf",
    "#637939", "#6b6ecf", "#9c9ede", "#d62728", "#8ca252", "#8c6d31", "#bd9e39",
    "#e7cb94", "#843c39", "#ad494a", "#d6616b", "#7b4173", "#a55194", "#ce6dbd",
    "#de9ed6"];

  inst_color = all_colors[cat_num % len(all_colors)]

  return inst_color

def add_cats(net, axis, cat_data):

  try:
    df = net.export_df()

    if axis == 'row':
      labels = df.index.tolist()
    elif axis == 'col':
      labels = df.columns.tolist()

    if 'title' in cat_data:
      inst_title = cat_data['title']
    else:
      inst_title = 'New Category'

    all_cats = cat_data['cats']

    # loop through all labels
    new_labels = []
    for inst_label in labels:

      if type(inst_label) is tuple:
        check_name = inst_label[0]
        found_tuple = True
      else:
        check_name = inst_label
        found_tuple = False

      if ': ' in check_name:
        check_name = check_name.split(': ')[1]

      # default to False for found cat, overwrite if necessary
      found_cat = inst_title + ': False'

      # check all categories in cats
      for inst_cat in all_cats:

        inst_names = all_cats[inst_cat]

        if check_name in inst_names:
          found_cat = inst_title + ': ' + inst_cat

      # add category to label
      if found_tuple is True:
        new_label = inst_label + (found_cat,)
      else:
        new_label = (inst_label, found_cat)

      new_labels.append(new_label)


    # add labels back to DataFrame
    if axis == 'row':
      df.index = new_labels
    elif axis == 'col':
      df.columns = new_labels

    net.load_df(df)

  except:
    print('error adding new categories')




