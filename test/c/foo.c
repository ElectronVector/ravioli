//
// Created by Matt on 11/10/2018.
//

#include "foo.h"

static int local_variable;
int global_variable;
int another_global;
static int another_local;

int if_else(int i) {
    if (i >= 0) {
        return i + 1;
    }
    else {
        return i - 1;
    }
}

int else_if(int i) {
    if (i >= 5) {
        return i + 1;
    }
    else if (i >= 0) {
        return i + 2;
    }
    else {
        return i - 1;
    }
}

int nested_if(int i) {
    if (i >= 0) {
        if (i >= 5) {
            return i + 2;
        }
        else {
            return i + 1;
        }
    }
    else {
        return i - 1;
    }
}

int nested_else_if(int i) {
    if (i >= 0) {
        if (i >= 5) {
            return i + 2;
        }
        else if (i >= 3) {
            return i + 4;
        }
        else {
            return i + 1;
        }
    }
    else {
        return i - 1;
    }
}

int nested_else_if_with_extra_statements(int i) {
    i = i + 1;
    if (i >= 0) {
        i = i + 1;
        if (i >= 5) {
            i = i + 1;
            return i + 2;
        }
        else if (i >= 3) {
            i = i + 1;
            return i + 4;
        }
        else {
            return i + 1;
        }
    }
    else {
        return i - 1;
    }
}

int no_decisions () {
    int a_local_variable = 0;
    return 0;
}

int compound_if(int i) {
    if ((i >= 0) && (i < 10)){
        return i + 2;
    }
    else {
        return i + 1;
    }
}

int compound_if_or(int i) {
    if ((i >= 0) || (i < 10)){
        return i + 2;
    }
    else {
        return i + 1;
    }
}

int multiple_compound_if(int i, int j) {
    if ((j == 3) || ((i >= 0) && (i < 10))){
        return i + 2;
    }
    else {
        return i + 1;
    }
}

int while_loop() {
    i = 0;
    while (i < 10){
        global_variable += 1;
        i++;
    }
}

int for_loop() {
    for (i = 0; i < 10; i++){
        global_variable += 1;
    }
}

int do_while_loop() {
    i = 0;
    do {
        global_variable += 1;
        i++;
    }while (i < 10);
}

int compound_while_loop(int j, int i) {
    i = 0;
    while ((j == 1) && (i < 10)) {
        global_variable += 1;
        i++;
        j++;
    }
}

int nested_for_loops() {
    for (i = 0; i < 10; i++){
        for (j = 0; j < 10; j++) {
            global_variable += 1;
        }
    }
}

int nested_loops_with_compound_conditional() {
    for (i = 0; i < 10; i++){
        int j = 0;
        while ((j < 10) && (i < 5)) {
            global_variable += 1;
            j++;
        }
    }
}

int a_complicated_example(int x, int y, int z) {
    int answer = 0;
    if (x > 15) {
        answer += 3;
    }
    else if ((x > 10) && (y > 5)) {
        answer += 4;
    }
    else if ((x > 5) && (y > 3) && (z > 1)) {
        answer += 1;
        result = 0;
        for (int i = 0, j = 0; (i < 10) && (result == 0); i++) {
            if ((global_variable == 15) || (another_global == 12)) {
                result = 1;
            }
        }
    }
    else {
        answer += 10;
    }
    return answer;
}

void switch_statement(int x) {
    switch (x) {
        case 1:
            global_variable += 2;
        case 2:
            global_variable += 3;
        default:
            global_variable += x;
    }
}