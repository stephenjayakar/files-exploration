# `basic_sync_test`

This test just created a logger that logs timestamp in ms, and calls an fsync, and then just times all the operations. It's pretty simple in that it only logs start time, and doesn't wrap any of the operations.

```
0.0 (ms): opening file
0.08893013000488281 (ms): writing to file
0.09012222290039062 (ms): syncing file
0.09417533874511719 (ms): finished
```

So the thing that took the longest _by far_ was opening the file. Syncing took also pretty long comparatively; over double the time as writing to the buffer. Note that I'm using an SSD.

# `sector_test`

This test was a bit more complicated. I opened two files, and initialized two strings, one larger than the other by 100 times. I _think_ this should still be much less than `SECTOR_SIZE`, whatever that is.

The test goes roughly like this:
1. Open two files
2. (timed) Write `meow` to f1, sync it
3. (timed) Write `meow` * 100 to f2, sync it
4. Compare results

I pre-initialized `meow` and `meow` * 100 so that it wouldn't meaningfully affect the results.

```
0.0 (ms): opening file 1
0.07486343383789062 (ms): opening file 2
0.11992454528808594 (ms): writing file 1
0.12087821960449219 (ms): syncing file 1
0.12278556823730469 (ms): writing file 2
0.12278556823730469 (ms): syncing file 2
0.1239776611328125 (ms): finished

Diffs
0.00286102294921875: time to write & sync to f1
0.0011920928955078125: time to write & sync to f2
```

This didn't make a lot of sense to me. Going to refactor a bit to support more repetitions.

### Added repetitions

After doing that, the results were much closer. Doing 1000 reps yielded a difference of like `0.00012612342834472656`ms, which is negligible:

```
r1: 0.0008313655853271484 ms
r2: 0.0007052421569824219 ms
diff: 0.00012612342834472656 ms
```

Interestingly, swapping the strings seemed to make no difference. So the theory is mostly confirmed. It is interesting that the speed seems to bias towards the earlier opened file.

