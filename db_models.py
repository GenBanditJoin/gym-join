from util import load_csv

class OuterRelationPage:

    def __init__(self, customer_id_set):
        self.customer_id_set = customer_id_set


class InnerRelationTuple:

    def __init__(self, order_id, customer_id):
        self.order_id = order_id
        self.customer_id = customer_id


class Table:

    def __init__(self, path, page_size, isOuter, reset=True):
        self.table = load_csv(path)
        self.current_index = 0
        self.size = len(self.table)
        self.page_size = page_size
        self.isOuter = isOuter
        self.page = 0
        self.reset = reset
    

    def reset_table(self):
        self.page = 0
        self.current_index = 0

        
    def next_page(self):
        if self.current_index == -1:
            return None
        start_index, end_index = self.__get_next_indexes()
        page = self.table[start_index:end_index]
        if len(page) > 0:
            self.page += 1

        if self.isOuter:
            return self.__set_outer_page(page)
        else:
            return self.__set_inner_tuples(page)
            
    def __set_outer_page(self, page):
        id_set = set()

        for val in self.table:
            id_set.add(val[0])
        
        if len(id_set) == 0:
            return None
        return OuterRelationPage(id_set)
    
    def __set_inner_tuples(self, page):
        inner_relation_list = []

        for val in page:
            ir = InnerRelationTuple(val[0], val[1])
            inner_relation_list.append(ir)

        if len(inner_relation_list) == 0:
            return None
        return inner_relation_list

    def __get_next_indexes(self):
        
        start_index = self.current_index
        if start_index + self.page_size + 1 <= self.size:
            end_index = start_index + self.page_size
            self.current_index = end_index
        else:
            end_index = self.size 
            if not self.isOuter and self.reset:
                self.current_index = 0
                #Reset the inner table 
                if start_index == end_index:
                    start_index = 0
                    end_index = start_index + self.page_size + 1
                    self.current_index = end_index
                else:
                    self.current_index = 0
            else:
                self.current_index = -1
        return start_index, end_index


def join(outer_page, inner_relation_tuples, results):
    count = 0
    for inner_tuple in inner_relation_tuples:

        if inner_tuple.customer_id in outer_page.customer_id_set:
            results.add(str(inner_tuple.customer_id + "-" + inner_tuple.order_id))
            count += 1
    return count


def join_all(outer_page, results):
    s = Table("data/order.tbl", 16, False, False)


    s_page  = s.next_page()
    count = 0
    while s_page:

        for inner_tuple in s_page:

            if inner_tuple.customer_id in outer_page.customer_id_set:
                results.add(str(inner_tuple.customer_id + "-" + inner_tuple.order_id))
            count += 1
        s_page  = s.next_page()
    return count



            
