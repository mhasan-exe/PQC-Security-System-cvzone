#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <time.h>
#include <math.h>
#include <stdatomic.h>
#include <unistd.h>
#define ALPHABET "abcdefghijklmnopqrstuvwxyz"
#define MAXLEN 32

atomic_ullong tries = 0;
atomic_int found = 0;
char secret[MAXLEN];
int len;

void increment(char *g, int start, int step) {
    unsigned long long local_tries = 0;
    while (!found) {
        local_tries++;
        if (strcmp(g, secret) == 0) {
            printf("\n✅ Found word: %s (after %llu tries)\n", g, local_tries);
            found = 1;
            return;
        }

        // increment like base-26
        for (int i = len - 1; i >= 0; i--) {
            g[i] += step;
            if (g[i] <= 'z') break;
            g[i] = 'a';
            if (i == 0) return; // end reached
        }

        tries++;
    }
}

void *worker(void *arg) {
    int start = *(int *)arg;
    char guess[MAXLEN];
    for (int i = 0; i < len; i++) guess[i] = 'a';
    guess[len] = '\0';
    guess[0] = 'a' + start;
    increment(guess, start, 1);
    return NULL;
}

int main() {
    printf("Enter your secret word: ");
    scanf("%31s", secret);
    len = strlen(secret);

    unsigned long long total = powl(26, len);
    printf("Target length: %d (%,llu combinations)\n", len, total);

    pthread_t t1, t2;
    int a = 0, b = 13; // split alphabet in half

    time_t start_time = time(NULL);

    pthread_create(&t1, NULL, worker, &a);
    pthread_create(&t2, NULL, worker, &b);

    while (!found) {
        sleep(1);
        double elapsed = difftime(time(NULL), start_time);
        double speed = tries / elapsed;
        double pct = (double)tries / total * 100.0;
        double eta = (total - tries) / (speed > 0 ? speed : 1);
        printf("\rProgress: %.2f%% (%llu tries, %.2f M/s, ETA %.0fs)   ",
               pct, (unsigned long long)tries, speed / 1e6, eta);
        fflush(stdout);
    }

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("\n\nDone.\n");
    return 0;
}




