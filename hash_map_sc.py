# Name: Suhrob Hasanov
# OSU Email: hasanovs@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/13/23
# Description: SC HashMap implementation  

from a6_include import (DynamicArray, LinkedList, hash_function_1,
                        hash_function_2, SLNode)

class HashMap:

    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor**2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds key/value pair to the hash map.
        """
        load_factor = self._size / self.get_capacity()

        # print(load_factor)
        if load_factor >= 1:
            self.resize_table(self.get_capacity() * 2)
        
        # Hash process to get index
        hash = self._hash_function(key)
        size = self.get_capacity()
        index = hash % size

        # If there is node in the linked list at this index with the same key, so need to overwrite
        if self._buckets[index].contains(key):
            node = self._buckets[index].contains(key)
            node.value = value
        # No two same keys
        else:
            self._buckets[index].insert(key, value) 
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets of the map.
        """
        counter = 0

        # iterating and counting empty buckets
        for i in range(self.get_capacity()):
            if self._buckets[i].length() == 0:
                counter += 1
        return counter

    def table_load(self) -> float:
        """
        Returns load factor of the hash map. 
        """
        load_factor = self._size / self.get_capacity()
        return load_factor

    def clear(self) -> None:
        """
        Clears the hashmap.
        """
        new_bucket = DynamicArray()
        # Adding placeholders to the array
        for i in range(self._capacity):
            new_bucket.append(LinkedList())
        self._buckets = new_bucket
        self._size = 0


    def resize_table(self, new_capacity: int) -> None:
            """
            Resizes the table with given new capacity.
            """
            # If new capacity is less than 1, do nothing
            if (new_capacity < 1):
                return

            # If new capacity is not prime, getting prime one
            if self._is_prime(new_capacity) is False:
                new_capacity = self._next_prime(new_capacity)

            # new bucket created
            copy_bucket = self._buckets
            copy_capacity = self._capacity 

            # Resetting the underlying array and its size
            self._buckets = DynamicArray()
            self._size = 0
           
            # adding SLLs tothe new bucket
            for _ in range(new_capacity):
                self._buckets.append(LinkedList())

            self._capacity = new_capacity
            for i in range(copy_capacity): 
                # If empty 
                if copy_bucket[i].length() == 0:
                    continue
                # If not empty
                else:
                    sll = copy_bucket[i] 
                    # Iterating and "putting" the values from old map to new
                    for node in sll:
                        value = node.value
                        key = node.key
                        self.put(node.key, node.value)
            return

    def get(self, key: str):
        """
        Returns the value associated with passed key.
        """
        # Hash process to get index
        hash = self._hash_function(key)
        size = self.get_capacity()
        index = hash % size

        # If empty then return none
        if self._buckets[index].length() == 0:
            return None

        # Iterate till right node found
        sll = self._buckets[index]
        for node in sll:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns boolean depending whether key is in map.
        """
        if self._size == 0:
            return False
        # Hash process to get index
        hash = self._hash_function(key)
        size = self.get_capacity()
        index = hash % size

        if self._buckets[index].length() == 0:
            return False
        
        sll = self._buckets[index]
        for node in sll:
            if node.key == key:
                return True
            node = node.next
        return False


    def remove(self, key: str) -> None:
        """
        Removes key/value pair from the map.
        """
        # If empty, then just return
        if self._size == 0:
            return 
        
        # Hash process to get index
        hash = self._hash_function(key)
        size = self.get_capacity()
        index = hash % size

        if self._buckets[index].length() == 0:
            return 
        # Iterate till right node found
        sll = self._buckets[index]
        for node in sll:
            if node.key == key:
                self._buckets[index].remove(key)
                self._size -= 1
                return
            node = node.next
        return 

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns DynamicArray of key/value pairs in map.
        """
        return_array = DynamicArray()

        for i in range(self.get_capacity()):
            if self._buckets[i].length() == 0:
                continue
            else:
                # Iterate till right node found
                sll = self._buckets[i]
                for node in sll:
                    key_pair = (node.key, node.value)
                    return_array.append(key_pair)    
                    node = node.next
        return return_array



def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns tuple of Dynamic array which contains mode elements and integer which is frequency.
    """
    map = HashMap()
    frequency = 1
    mode_items = DynamicArray()
    
    # Iterating over the passed DA and adding it to map
    for i in range(da.length()):
        # If if element is not in map
        if map.contains_key(da[i]) is False:
            map.put(da[i], 1)
            # if element mode, which is 1 is equal to the highest frequency, add element to mode list
            if frequency == 1:
                mode_items.append(da[i])
        # If element is in map, then we increment the value (frequency)
        else:
           value =  map.get(da[i]) + 1
           # If value is higher than frequency, update frequency
           if value > frequency:
               frequency = value
               # Reset the mode list and add the element with highest frequency
               mode_items = DynamicArray()
               mode_items.append(da[i])
           # If value and frequency is equal, just adding the element to the mode list
           elif value == frequency:
               mode_items.append(da[i])
           # adding the element from DA to the map
           map.put(da[i], value)
            
    return mode_items, frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # # print("\nPDF - find_mode example 1")
    # # print("-----------------------------")
    # da = DynamicArray([ "apple", "apple", "peach", "grape", "melon", "peach"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")



    

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
    #               m.get_capacity())
    #         # print(m.get_capacity())

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
    #               m.get_capacity())

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))

    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'),
    #       m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(),  m.get_capacity(), m.get('key1'),
    #       m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())

    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)

    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')

    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity,  result, m.get_size(), m.get_capacity(),
    #           round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))

    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')

    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())

    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(['D', 'BlnKnizHe', 'wJDvg', 'QEH', 'jo', 'bd', 'UgVUE'])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = ([
        "Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu",
        "Ubuntu", "Ubuntu"
    ], ["one", "two", "three", "four", "five"], [
        "2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"
    ])

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
