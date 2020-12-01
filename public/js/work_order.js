const encode = encodeURIComponent; // bc i dont want to write the whole thing every time
const WO_SESSION_KEY = "_work_orders";

async function listWO(params) {
  let url;
  if (params === undefined) {
    url = "/api/workorders";
  } else {
    let query = new URLSearchParams(params);
    url = `/api/workorders?${query}`;
  }
  return await fetch(url)
    .then((resp) => resp.json())
    .then((json) => {
      let results = json["workorders"].map((raw) => new WorkOrder(raw));
      return results;
    });
}

class WorkOrder {
  constructor(data) {
    if (typeof data === "number") {
      this.num = data;
    } else {
      for (const attr in data) {
        this[attr] = data[attr];
      }
    }
  }

  init() {
    fetch(`/api/workorder/${this.num}`)
      .then((resp) => {
        if (resp.status != 200) {
          console.log("Could not find work order " + data);
          throw resp.json();
        }
        return resp.json();
      })
      .then((json) => {
        console.log(data);
        if (json.num != this.num) {
          console.log("Error: backend returned the wrong work order number");
        }
        this.bartdept = json.bartdept;
        this.description = json.description;
        this.status = json.status;
      })
      .catch((error) => console.log("got error:", error));
  }

  async reportDate() {
    return await fetch(`/api/workorder/${this.num}/report_date`)
      .catch((err) => console.log("Work order report date error:", err))
      .then((resp) => {
        console.log(resp.status);
        return resp.json();
      });
  }
}

class WorkOrderTable {
  constructor(tableID, limit) {
    if (limit === undefined) {
      this.limit = 20;
    } else {
      this.limit = limit;
    }
    this.table = document.getElementById(tableID);
    this.visable = false;
    this.workorder = [];
  }

  render() {
    this.visable = true;
    this.fetchTable(10);
  }

  toggle() {
    if (this.visable) {
      this.table.innerHTML = "";
    } else {
      this.fetchTable();
    }
    this.visable = !this.visable;
  }

  fetchTable(lim) {
    if (lim === undefined) {
      lim = 10;
    }
    // if there are assets in the cache then use them
    this.table.innerHTML += `<tr>
      <th>Work Order</th>
      <th>Department</th>
      <th>Status</th>
    </tr>`;
    if (this.workorder.length != 0) {
      this.showWorkOrder(this.workorder);
      return;
    }
    listWorkOrder({ limit: lim, offset: 0 })
      .then((workorder) => {
        this.workorder = workorder; // cache the result
        this.showWorkOrder(workorder);
      })
      .catch((error) => {
        console.log(error);
        this.table.innerHTML = `
          <p class="errorMsg"><span style="color:red;">Error</span>: Could not get Work Orders</p>`;
      });
  }

  showWorkOrder(workorder) {
    for (let i = 0; i < workorder.length; i++) {
      let workorder = workorder[i];
      this.table.innerHTML += `<tr>
        <td><a href="/workorder?workordernum=${workorder.num}">${workorder.num}</a></td>
        <td>${workorder.bartdept}</td>
        <td>${workorder.status}</td>
      </tr>`;
    }
    if (this.workorder.length >= this.limit) {
      return;
    }
    const id = "showMoreWorkOrders";
    this.table.innerHTML += `<button id="${id}">show more...</button>`;
    const more = document.getElementById(id);
    const callback = (event) => {
      listWorkOrder({ limit: 10, offset: this.workorder.length }).then(
        (workorder) => {
          more.removeEventListener("click", callback); // remove itself
          this.table.removeChild(more);
          this.workorder = this.workorder.concat(workorder);
          this.showWorkOrder(workorder); // render new and add the more button
        }
      );
    };
    // add the click handler
    more.addEventListener("click", callback);
  }
}
