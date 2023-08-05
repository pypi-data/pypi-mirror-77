(async () => {
  await sodium.ready;

  const key = sodium.from_base64(window.location.hash.substring(1));

  const post = (node) => {
    document.body.insertBefore(node, document.body.firstChild);
    while (document.body.children.length > MAX) {
      document.body.lastChild.remove();
    }

    node.offsetWidth = node.offsetWidth;
    node.classList.add("created");

    window.scrollTo(0, 0);
  };

  const reconnect = async () => {
    const line = document.createElement("div");
    line.textContent = "Lost connection, reconnecting";
    post(line);
    await new Promise((resolve) => setTimeout(resolve, 10000));
    connect();
  };

  const connect = () => {
    let last = "-1";
    const ws = new WebSocket("ws://ADDRESS/ws");
    ws.onopen = async (event) => {
      ws.send(last);
    };
    ws.onmessage = async (event) => {
      const predata = sodium.from_base64(event.data);
      const nonce = predata.slice(0, sodium.crypto_secretbox_NONCEBYTES);
      const ciphertext = predata.slice(sodium.crypto_secretbox_NONCEBYTES);
      const data = JSON.parse(
        new TextDecoder().decode(
          sodium.crypto_secretbox_open_easy(ciphertext, nonce, key)
        )
      );
      console.log(data);

      const container = document.createElement("div");
      container.classList.add("message");
      const date = document.createElement("div");
      date.classList.add("date");
      date.textContent = data.date;
      const name = document.createElement("div");
      name.classList.add("name");
      name.textContent = data.name;
      const summary = document.createElement("div");
      summary.classList.add("summary");
      summary.textContent = data.summary;
      const body = document.createElement("div");
      body.classList.add("body");
      body.textContent = data.body;
      if (body.textContent.length > 200) {
        body.textContent = body.textContent.substring(0, 200) + "...";
      }
      container.appendChild(date);
      container.appendChild(name);
      container.appendChild(summary);
      container.appendChild(body);

      post(container);
      last = container.id;
    };
    ws.onclose = reconnect;
  };

  connect();
})();
