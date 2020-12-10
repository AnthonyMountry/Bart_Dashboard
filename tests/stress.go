package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"sync"
	"time"
)

func main() {

	var (
		n         int64 = 10
		closeConn bool
		compress  bool
		path      string
		client    = http.Client{
			Timeout: time.Minute,
		}
	)
	flag.Int64Var(&n, "n", n, "make n requests")
	flag.StringVar(&path, "path", "", "endpoint to test")
	flag.BoolVar(&closeConn, "close", closeConn, "tell the server to close the connection")
	flag.BoolVar(&compress, "compress", compress, "ask the server to compres the response")
	flag.Parse()

	u, err := url.Parse(path)
	if err != nil {
		log.Fatal(err)
	}

	var (
		resp *http.Response
		t    = time.Now()
		req  = http.Request{
			Method: "GET",
			Close:  closeConn,
			URL: &url.URL{
				Scheme:   "http",
				Host:     "localhost:5000",
				Path:     u.Path,
				RawQuery: u.RawQuery,
			},
			Header: http.Header{},
		}
		wg      sync.WaitGroup
		i       int64
		w       int64
		workers int64 = 300
		ch            = make(chan int64, workers)
	)
	if compress {
		req.Header.Set("Accept-Encoding", "br")
	}

	wg.Add(1)
	go func() {
		wg.Wait()
		close(ch)
	}()
	for i < n {
		for w = i; w < workers && i < n; w++ {
			wg.Add(1)
			go func(a int64) {
				tm := time.Now()
				defer wg.Done()
				resp, err = client.Do(&req)
				if err != nil {
					panic(err)
				}
				if resp.StatusCode != 200 {
					fmt.Println(resp.Status)
				}
				err = resp.Body.Close()
				if err != nil {
					panic(err)
				}
				ch <- time.Now().Sub(tm).Nanoseconds()
			}(i)
			i++
		}
	}

	wg.Done()
	var (
		count       = 0
		total int64 = 0
	)
	for r := range ch {
		count++
		total += r
	}

	n = int64(count)
	elapsed := time.Now().Sub(t)
	result := time.Duration(total)
	fmt.Println("requests made:   ", n)
	fmt.Println("total wait time: ", result)
	fmt.Println("per request:     ", time.Duration(result.Nanoseconds()/n))
	fmt.Println("elapsed:         ", elapsed)
	fmt.Println("response latency:", time.Duration(elapsed.Nanoseconds()/n))
}
