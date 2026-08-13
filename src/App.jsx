import './App.css'
import { useEffect, useState } from 'react'

function App() {
  const [products, setProducts] = useState([])

  const [form, setForm] = useState({
    name: '',
    material: '',
    purity: '',
    weight:'',
    price: '',
    category: ''
  })

  const [message, setMessage] = useState('')

  // Get products from FastAPI
  const loadProducts = () => {
    fetch('https://jewelhub-kucc.onrender.com/products')
      .then(response => response.json())
      .then(data => setProducts(data))
      .catch(error => console.error('Error:', error))
  }

  useEffect(() => {
    loadProducts()
  }, [])

  // Handle input changes
  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value
    })
  }

  // Add product
  const addProduct = (event) => {
    event.preventDefault()

    fetch('https://jewelhub-kucc.onrender.com/products', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: form.name,
        material: form.material,
        purity: form.purity,
        weight: Number(form.weight),
        price: Number(form.price),
        category: form.category
      })
    })
      .then(response => response.json())
      .then(data => {
        setMessage(data.message)

        setForm({
          name: '',
          material: '',
          purity: '',
          weight: '',
          price: '',
          category: ''
        })

        loadProducts()
      })
      .catch(error => {
        console.error('Error:', error)
        setMessage('Failed to add product')
      })
  }

  return (
    <div className="app">

      {/* Header */}
      <header className="header">

        <div className="logo">
          💎 JewelHub
        </div>

        <nav>
          <a href="#">Home</a>
          <a href="#">Jewellery</a>
          <a href="#">Categories</a>
          <a href="#">Sell Jewellery</a>
        </nav>

        <div className="header-actions">
          <button>🔍</button>
          <button>🛒</button>
          <button>Login</button>
        </div>

      </header>


      {/* Hero Section */}
      <section className="hero">

        <div>

          <h1>Find Your Perfect Jewellery</h1>

          <p>
            Discover beautiful jewellery from trusted sellers
            across our marketplace.
          </p>

          <div className="search-box">

            <input
              type="text"
              placeholder="Search jewellery..."
            />

            <button>Search</button>

          </div>

        </div>

      </section>


      {/* Categories */}
      <section className="section">

        <h2>Shop by Category</h2>

        <div className="categories">

          <div className="category">
            💍
            <p>Rings</p>
          </div>

          <div className="category">
            📿
            <p>Necklaces</p>
          </div>

          <div className="category">
            ✨
            <p>Earrings</p>
          </div>

          <div className="category">
            🔗
            <p>Chains</p>
          </div>

          <div className="category">
            🪙
            <p>Bangles</p>
          </div>

        </div>

      </section>


      {/* Seller Add Product */}
      <section className="section">

        <h2>Sell Your Jewellery</h2>

        <form onSubmit={addProduct}>

          <input
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="Product name"
            required
          />

          <input
            name="material"
            value={form.material}
            onChange={handleChange}
            placeholder="Material (Gold, Silver...)"
            required
          />

          <input
            name="purity"
            value={form.purity}
            onChange={handleChange}
            placeholder="Purity (22K, 18K...)"
            required
          />
          <input
            name="weight"
            type="number"
            step="0.01"
            value={form.weight}
            onChange={handleChange}
            placeholder="Weight in grams"
            required
          />
          <input
            name="price"
            type="number"
            value={form.price}
            onChange={handleChange}
            placeholder="Price"
            required
          />
          
          <input
            name="category"
            value={form.category}
            onChange={handleChange}
            placeholder="Category"
            required
          />

          <button type="submit">
            Add Product
          </button>

        </form>

        {message && <p>{message}</p>}

      </section>


      {/* Products */}
      <section className="section">

        <h2>Featured Jewellery</h2>

        <div className="products">

          {products.map((product) => (

            <div className="product" key={product.name}>

              <div className="product-image">
                💎
              </div>

              <h3>{product.name}</h3>

              <p>
                {product.purity} {product.material} • {product.weight} g
              </p>

              <strong>
                ₹{product.price.toLocaleString('en-IN')}
              </strong>

              <button>
                View Product
              </button>

            </div>

          ))}

        </div>

      </section>

    </div>
  )
}

export default App