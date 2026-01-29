const product_data = [
  { category: "상의", brand: "Supreme", product: "슈프림 박스로고 후드티", price: "390,000원" },
  { category: "하의", brand: "DIESEL", product: "디젤 트랙 팬츠", price: "188,000원" },
  { category: "신발", brand: "Nike", product: "에어포스 1", price: "137,000원" },
  { category: "패션잡화", brand: "Music&Goods", product: "빵빵이 키링", price: "29,000원" }
];

const tableBody = document.getElementById("product_data_Table");
const searchBtn = document.getElementById("searchBtn");
const searchInput = document.getElementById("searchInput");
const categorySelect = document.getElementById("categorySelect");

function renderTable(data) {
  tableBody.innerHTML = "";

  data.forEach(item => {
    const row = tableBody.insertRow();
    row.insertCell(0).innerText = item.category;
    row.insertCell(1).innerText = item.brand;
    row.insertCell(2).innerText = item.product;
    row.insertCell(3).innerText = item.price;
  });
}

renderTable(product_data);

searchBtn.addEventListener("click", () => {
  const keyword = searchInput.value.toLowerCase();
  const category = categorySelect.value;

  const filtered = product_data.filter(item => {
    const matchProduct = item.product.toLowerCase().includes(keyword);
    const matchCategory = category ? item.category === category : true;
    return matchProduct && matchCategory;
  });

  renderTable(filtered);
});
