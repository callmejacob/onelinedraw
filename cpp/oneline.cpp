#include <iostream>
#include <vector>
#include <stack>

// map
int M = 6;
int N = 6;
int* map;
int* temp;
int temp_count;
int start_i = 0;
int start_j = 0;

// record
std::stack<int> avail_stack;
std::stack<int> avail_index_stack;
std::vector<int> step_stack;
int step_cur_index = 0;

int get_index(int pos_i, int pos_j) {
    if (pos_i < 0 || pos_i >= M || pos_j < 0 || pos_j >= N) return -1;
    return pos_i * N + pos_j;
}

void get_pos(int index, int& pos_i, int& pos_j) {
    pos_i = index / N;
    pos_j = index % N;
}

void print_index(int index) {
    int pos_i = 0;
    int pos_j = 0;
    get_pos(index, pos_i, pos_j);
    //std::cout << "[" << pos_i << ", " << pos_j << "]" << std::endl;
}

bool get_avail_items(int index) {
    temp_count = 0;
    
    int i = 0;
    int j = 0;
    get_pos(index, i, j);

    int direct[4];
    direct[0] = get_index(i - 1, j);
    direct[1] = get_index(i + 1, j);
    direct[2] = get_index(i, j - 1);
    direct[3] = get_index(i, j + 1);

    for (int d = 0; d < 4; d++) {
        // 获取索引
        int cur_index = direct[d];
        if (cur_index == -1) continue;

        // 获取坐标
        int ii = 0;
        int jj = 0;
        get_pos(cur_index, ii, jj);

        // 是否超出地图了
        if (ii < 0 || ii >= M || jj < 0 || jj >= N) continue;

        // 障碍物
        if (map[ii * N + jj] == 0) continue;

        // 是否已经走过了
        bool is_steped = false;
        for (int i = 0; i < step_cur_index; i++) {
            if (step_stack[i] == cur_index) is_steped = true;
        }
        if (is_steped) continue;

        // 记录当前数值
        temp[temp_count++] = cur_index; 
    }

    return (temp_count > 0);
}

bool push_avail_items(int index) {
    if (temp_count == 0) return false;

    for (int i = 0; i < temp_count; i++) {
        avail_stack.push(temp[i]);
        avail_index_stack.push(step_cur_index);       
        //std::cout << "push index: " << temp[i] << " and it's step_index is: " << step_cur_index << std::endl;
        print_index(temp[i]);
    }
    return true;
}

void print_avail_items() {
    while (!avail_stack.empty()) {
        int index = avail_stack.top();
        avail_stack.pop();

        int pos_i = 0;
        int pos_j = 0;
        get_pos(index, pos_i, pos_j);
        //std::cout << "[" << pos_i << ", " << pos_j << "]" << std::endl;
    }
}

int main(int argc, char** argv) {
    if (argc > 4) {
        M = std::atoi(argv[1]);
        N = std::atoi(argv[2]);
        start_i = std::atoi(argv[3]) - 1;
        start_j = std::atoi(argv[4]) - 1;
        //std::cout << "args: M-" << M << " N-" << N << " SI-" << start_i << " SJ-" << start_j << std::endl;
    }

    // init
    map = new int[M * N];
    temp = new int[M * N];

    //std::cout << "one draw begin" << std::endl;

    // 初始化map
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            map[i * N + j] = 1;
        }
    }

    for (int i = 5; i < argc; i += 2) {
        int row = std::atoi(argv[i]) - 1;
        int col = std::atoi(argv[i + 1]) - 1;
        map[row * N + col] = 0;
        //std::cout << "hole: " << row << " " << col << std::endl;
    }

    int start_index = get_index(start_i, start_j);
    //std::cout << "start index: " << start_index << std::endl;


    // 计算有效个数的总数目
    int total_num = 0;
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            if (map[i * N + j]) total_num++;
        }
    }
    //std::cout << "total_num: " << total_num << std::endl;

    // 初始化记录堆栈
    step_stack.reserve(total_num);
    step_stack[step_cur_index++] = start_index;

    get_avail_items(start_index);
    push_avail_items(start_index);

    // 寻找路径
    while (!avail_stack.empty()) {
        int seed = avail_stack.top();
        int seed_index = avail_index_stack.top();
        if (seed_index >= total_num) break;

        avail_stack.pop();
        avail_index_stack.pop();

        //std::cout << "Get seed: " << seed << " And it's index: " << seed_index << std::endl;
        print_index(seed);

        bool is_seed_avail = get_avail_items(seed);
        if (!is_seed_avail) {
            if (seed_index == total_num - 1) {
                //std::cout << "find a path!" << std::endl;
		step_stack[step_cur_index++] = seed;
                break;
            } else {
                // 抹去走错的路...
                step_cur_index = 0;
                if (!avail_index_stack.empty()) {
                    step_cur_index = avail_index_stack.top();
                }
            }
        } else {
            // 在当前步上记录seed，同时增长步长，将下一步的有效种子都记录下来
            step_stack[step_cur_index++] = seed;
            push_avail_items(seed);
        }      
    }

    // 打印路径
    for (int i = 0; i < step_cur_index; i++) {
        int index = step_stack[i];
        int pos_i = 0;
        int pos_j = 0;
        get_pos(index, pos_i, pos_j);
 
        // (x, y)
        std::cout << pos_j << " " << (M - pos_i) << std::endl;
    }

    // clean
    delete map;
    delete temp;

    return 0;
}
