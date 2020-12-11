const newelem = (tag, data) => {
  let el = document.createElement(tag);
  el.innerHTML = data;
  return el;
};

function createHeader(colnames) {
  let head = document.createElement("thead");
  let tr = document.createElement("tr");
  for (let i in colnames) {
    let e = newelem("th", colnames[i]);
    e.setAttribute("scope", "col");
    e.classList.add("th-sm");
    tr.appendChild(e);
  }
  head.appendChild(tr);
  return head;
}

function toTitle(s) {
  return s
    .split("_")
    .map((e) => e[0].toUpperCase() + e.slice(1, e.length))
    .join(" ");
}

class Table {
  constructor(id, options) {
    this.rowlimit = options["limit"] || 10;
    this.start = 0;

    this.table = document.getElementById(id);
    this.head = createHeader(options.colnames);
    this.body = null;
    this.objs = [];
    this.rows = [];
    this.page = 0;

    this.column_mapping = options["column_mapping"] || null;

    if ("renderCell" in options) {
      this.renderCell = options["renderCell"];
    } else {
      this.renderCell = (tag, data, key) => newelem(tag, data[key]);
    }

    if ("rows" in options) {
      this.setRows(options["rows"]);
    }

    this.counter = document.getElementById(`${id}-current`);
    let next = document.getElementById(`${id}-next`);
    let prev = document.getElementById(`${id}-prev`);
    let first = document.getElementById(`${id}-first`);
    let last = document.getElementById(`${id}-last`);
    if (next == null || prev == null) {
      return;
    }

    const pagenum = () => {
      next.innerHTML = this.page + 2;
      prev.innerHTML = this.page;
    };

    next.addEventListener("click", (event) => {
      prev.disabled = false;
      next.disabled = !this.next();
      pagenum();
    });
    prev.addEventListener("click", (event) => {
      next.disabled = false;
      prev.disabled = this.start <= this.rowlimit;
      this.prev();
      pagenum();
    });
    if (first != null) {
      first.addEventListener("click", (event) => {
        this.first();
        prev.disabled = true;
        next.disabled = false;
        pagenum();
      });
    }
    if (last != null) {
      last.addEventListener("click", (event) => {
        this.last();
        next.disabled = true;
        prev.disabled = false;
        pagenum();
      });
    }
  }

  render() {
    if (this.rows.length == 0) {
      this.body = newelem("p", "no results");
      this.table.appendChild(this.body);
      return;
    }
    let stop = this.start + this.rowlimit;
    this.body = null;
    this.body = document.createElement("tbody");
    for (let i = this.start; i < this.rows.length && i < stop; i++) {
      this.body.appendChild(this.rows[i]);
    }
    this.table.appendChild(this.head);
    this.table.appendChild(this.body);
    this.counter.innerHTML = this.page + 1;
  }

  teardown() {
    try {
      if (this.body !== null) {
        this.table.removeChild(this.body);
      }
      this.table.removeChild(this.head);
    } catch (err) {
      console.log(err);
    }
    this.body = null;
  }

  traverse(n) {
    this.page += n;
    this.start += this.rowlimit * n;
    this.table.removeChild(this.body);
    this.render();
  }

  next() {
    if (this.start + this.rowlimit >= this.rows.length) {
      return false;
    }
    this.traverse(1);
    return this.hasNext();
  }

  prev() {
    if (this.start <= 0) {
      return false;
    }
    this.traverse(-1);
    return this.atEnd();
  }

  last() {
    if (this.start + this.rowlimit >= this.rows.length) {
      return false;
    }
    this.page = Math.round(this.rows.length / this.rowlimit) - 1;
    this.start = this.rowlimit * this.page;
    this.table.removeChild(this.body);
    this.render();
    return true;
  }

  first() {
    if (this.start <= 0) {
      return false;
    }
    this.page = 0;
    this.start = 0;
    this.table.removeChild(this.body);
    this.render();
    return this.atEnd();
  }

  hasNext() {
    return this.start + this.rowlimit < this.rows.length;
  }

  atEnd() {
    return this.page == 1 || this.page == 0;
  }

  collapse() {
    this.table.removeChild(this.head);
    this.table.removeChild(this.body);
    this.body = null;
  }

  setRows(rows) {
    this.rows = [];
    this.objs = [];
    for (let i in rows) {
      this.addRow(rows[i]);
    }
  }

  addRow(obj) {
    this.rows.push(this._newRow(obj));
    this.objs.push(obj);
  }

  _newRow(obj) {
    let row = document.createElement("tr");
    if (this.column_mapping !== null) {
      for (i in this.column_mapping) {
        row.appendChild(this.renderCell("td", obj, this.column_mapping[i]));
      }
    } else {
      for (let attr in obj) {
        row.appendChild(this.renderCell("td", obj, attr));
      }
    }
    return row;
  }
}
