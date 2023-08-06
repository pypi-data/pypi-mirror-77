"""이 파일은 srproject.py 모듈이며, print_lol() 함수 하나를 제공합니다. 이 함수는 포함된
리스트가 있을 경우 그것을 포함해서 리스트의 모든 항목을 화면에 출력합니다."""

def print_lol(the_list, indent=False, level=0):
    """이 함수는 the_list라는 이름의 인자를 갖고 있으며, 파이썬 리스트를 받습니다. 이 리스트는
    리스트도 항목으로 포함할 수 있습니다. 매 라인마다 리스트에 있는 데이터 항목이 하나씩
    재귀적으로 화면에 출력됩니다.
    두 번째 인자 level은 중첩된 리스트에서 탭을 추갛기 위해 사용됩니다."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
            print(each_item)