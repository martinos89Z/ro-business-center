function toggleMenu() {
  document.getElementById('mobileMenu').classList.toggle('open');
}

function updateActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  let current = '';
  sections.forEach(section => {
    const sectionTop = section.offsetTop - 120;
    if (window.scrollY >= sectionTop) {
      current = section.id;
    }
  });
  document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === '#' + current);
  });
}

const BUSINESS_EMAIL = 'guinnoukoami@gmail.com';
const BUSINESS_WHATSAPP = window.WHATSAPP_PHONE || '22892888759';

function toggleScrollTop() {
  const btn = document.getElementById('scrollTop');
  if (btn) btn.classList.toggle('show', window.scrollY > 400);
}

function showSuccessMessage(selector) {
  const success = document.getElementById(selector);
  if (success) {
    success.style.display = 'block';
    setTimeout(() => { success.style.display = 'none'; }, 5000);
  }
}

function openMail(subject, body) {
  const greeting = 'Bonjour Mr RO Business Center, ';
  const text = encodeURIComponent(greeting + body);
  const mailto = `mailto:${BUSINESS_EMAIL}?subject=${encodeURIComponent(subject)}&body=${text}`;
  window.open(mailto, '_blank');
}

function openWhatsApp(message) {
  const greeting = 'Bonjour Mr RO Business Center, ';
  const text = encodeURIComponent(greeting + message);
  const wa = `https://wa.me/${BUSINESS_WHATSAPP}?text=${text}`;
  window.open(wa, '_blank', 'noopener,noreferrer');
}

function buildProductOrderMessage(data) {
  const lines = [];
  if (data.product) lines.push(`Produit: ${data.product}`);
  if (data.category) lines.push(`Catégorie: ${data.category}`);
  if (data.brand) lines.push(`Marque: ${data.brand}`);
  if (data.processor) lines.push(`Processeur: ${data.processor}`);
  if (data.ram) lines.push(`RAM: ${data.ram}`);
  if (data.storage) lines.push(`Stockage: ${data.storage}`);
  if (data.state) lines.push(`État: ${data.state}`);
  if (data.price) lines.push(`Prix: ${data.price} FCFA`);
  if (data.availability) lines.push(`Disponibilité: ${data.availability}`);
  if (data.desc) lines.push(`Description: ${data.desc}`);
  return lines.join('\n');
}

// Opens product modal with populated data
function openProductModal(data) {
  const modal = document.getElementById('productModal');
  if (!modal) return;
  const imgEl = document.getElementById('modalImage');
  const titleEl = document.getElementById('modalTitle');
  const descEl = document.getElementById('modalDesc');
  const brandEl = document.querySelector('#modalBrand span');
  const processorEl = document.querySelector('#modalProcessor span');
  const ramEl = document.querySelector('#modalRam span');
  const storageEl = document.querySelector('#modalStorage span');
  const stateEl = document.querySelector('#modalState span');

  if (imgEl && data.img) imgEl.src = data.img;
  if (titleEl) titleEl.textContent = data.title || 'Produit';
  if (descEl) descEl.textContent = data.desc || '';
  if (brandEl) brandEl.textContent = data.brand || '';
  if (processorEl) processorEl.textContent = data.processor || '';
  if (ramEl) ramEl.textContent = data.ram || '';
  if (storageEl) storageEl.textContent = data.storage || '';
  if (stateEl) stateEl.textContent = data.state || '';

  // Set up Whatsapp button for this product modal (id: modalWhatsappBtn)
  const pWa = document.getElementById('modalWhatsappBtn');
  const pView = document.getElementById('modalViewBtn');
  // remove previous handlers
  if (pWa) {
    pWa.onclick = (e) => {
      e.preventDefault();
      const productData = {
        product: data.title,
        category: data.category,
        brand: data.brand,
        processor: data.processor,
        ram: data.ram,
        storage: data.storage,
        state: data.state,
        desc: data.desc
      };
      openWhatsApp(buildProductOrderMessage(productData) + (data.img ? `\nImage: ${data.img}` : ''));
    };
  }

  if (pView) {
    pView.onclick = (e) => {
      e.preventDefault();
      if (data.id) {
        window.location.href = `/product/${data.id}`;
      } else if (data.link) {
        window.location.href = data.link;
      }
    };
  }

  modal.setAttribute('aria-hidden', 'false');
}

let pendingForm = null;
let pendingFormData = null;

function showActionModal(title, message) {
  const modal = document.getElementById('actionModal');
  if (!modal) return;
  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalMessage').textContent = message;
  modal.style.display = 'flex';
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}

function hideActionModal() {
  const modal = document.getElementById('actionModal');
  if (!modal) return;
  modal.style.display = 'none';
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

async function handleFormSend(channel) {
  if (!pendingForm || !pendingFormData) return;
  const data = pendingFormData;

  const payload = pendingForm === 'inscription'
    ? {
        prenom: data.prenom,
        nom: data.nom,
        tel: data.tel,
        email: data.email,
        formation: data.formation,
        message: data.message
      }
    : {
        name: data.nom,
        message: data.message,
        email: data.email,
        phone: data.contact,
        subject: data.sujet
      };

  const endpoint = pendingForm === 'inscription' ? '/inscription' : '/contact';

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const result = await response.json();
    if (!response.ok || result.status !== 'success') {
      throw new Error(result.message || 'Erreur lors de l\'envoi.');
    }
  } catch (error) {
    alert(`Impossible d\'envoyer la demande : ${error.message}`);
    return;
  }

  let subject;
  let body;
  if (pendingForm === 'inscription') {
    subject = `Demande d'inscription - ${data.formation}`;
    body = `Prénom: ${data.prenom}\nNom: ${data.nom}\nTéléphone: ${data.tel}\nEmail: ${data.email || 'Non renseigné'}\nFormation: ${data.formation}\nMessage: ${data.message || 'Aucun message'}`;
  } else {
    subject = `Demande de contact - ${data.sujet || 'Formulaire de contact'}`;
    body = `Nom: ${data.nom}\nContact: ${data.contact}\nEmail: ${data.email || 'Non renseigné'}\nSujet: ${data.sujet}\nMessage: ${data.message}`;
  }

  if (channel === 'email') {
    openMail(subject, body);
  } else if (channel === 'whatsapp') {
    openWhatsApp(body);
  }

  if (pendingForm === 'inscription') {
    showSuccessMessage('inscSuccess');
    document.getElementById('inscriptionForm').reset();
  } else if (pendingForm === 'contact') {
    showSuccessMessage('contactSuccess');
    document.getElementById('contactForm').reset();
  }

  pendingForm = null;
  pendingFormData = null;
  hideActionModal();
}

function openWhatsAppForProduct(button) {
  const productData = {
    product: button.dataset.product || 'Produit',
    category: button.dataset.category || button.closest('[data-category]')?.dataset.category || 'Produit',
    brand: button.dataset.brand || button.closest('[data-brand]')?.dataset.brand || '',
    processor: button.dataset.processor || button.closest('[data-processor]')?.dataset.processor || '',
    ram: button.dataset.ram || button.closest('[data-ram]')?.dataset.ram || '',
    storage: button.dataset.storage || button.closest('[data-storage]')?.dataset.storage || '',
    state: button.dataset.state || button.closest('[data-state]')?.dataset.state || '',
    price: button.dataset.price || button.closest('[data-price]')?.dataset.price || '',
    availability: button.dataset.availability || button.closest('[data-availability]')?.dataset.availability || '',
    desc: button.dataset.desc || button.closest('[data-desc]')?.dataset.desc || ''
  };

  const itemMessage = buildProductOrderMessage(productData);
  const message = `Je souhaite commander ce produit.\n${itemMessage}\nMerci de me recontacter.`;
  openWhatsApp(message);
}

async function submitInscription(event) {
  event.preventDefault();
  const prenom = document.getElementById('prenom').value.trim();
  const nom = document.getElementById('nom').value.trim();
  const tel = document.getElementById('tel').value.trim();
  const email = document.getElementById('email').value.trim();
  const formation = document.getElementById('formation').value;
  const message = document.getElementById('inscMessage').value.trim();
  if (!prenom || !tel || !formation) {
    alert('Veuillez remplir les champs obligatoires : Prénom, Téléphone et Formation.');
    return;
  }
  pendingForm = 'inscription';
  pendingFormData = { prenom, nom, tel, email, formation, message };
  showActionModal('Envoyer votre demande d’inscription', 'Choisissez comment vous souhaitez l’envoyer : Email ou WhatsApp.');
}

async function submitContact(event) {
  event.preventDefault();
  const nom = document.getElementById('cNom').value.trim();
  const contact = document.getElementById('cContact').value.trim();
  const sujet = document.getElementById('cSujet').value;
  const message = document.getElementById('cMessage').value.trim();
  const email = document.getElementById('cEmail')?.value.trim() || '';
  if (!nom || !message) {
    alert('Veuillez remplir votre nom et votre message.');
    return;
  }
  pendingForm = 'contact';
  pendingFormData = { nom, contact, sujet, message, email };
  showActionModal('Envoyer votre message de contact', 'Choisissez comment vous souhaitez l’envoyer : Email ou WhatsApp.');
}

function initPage() {
  updateActiveNav();
  document.querySelectorAll('#navbar, .nav-links, .hero-content, .hero-promo, .hero-badge').forEach(el => {
    el.classList.add('enter');
  });
  document.getElementById('inscriptionForm')?.addEventListener('submit', submitInscription);
  document.getElementById('contactForm')?.addEventListener('submit', submitContact);
  document.getElementById('modalEmailBtn')?.addEventListener('click', () => handleFormSend('email'));
  document.getElementById('modalWhatsAppBtn')?.addEventListener('click', () => handleFormSend('whatsapp'));
  document.getElementById('modalCancelBtn')?.addEventListener('click', hideActionModal);
  document.getElementById('modalOverlay')?.addEventListener('click', hideActionModal);
  document.querySelectorAll('.mobile-menu a').forEach(link => link.addEventListener('click', toggleMenu));
  document.getElementById('scrollTop')?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  document.querySelectorAll('[data-whatsapp-product="true"]').forEach(btn => {
    btn.addEventListener('click', () => openWhatsAppForProduct(btn));
  });
  const boutiqueSearch = document.getElementById('boutiqueSearch');
  if (boutiqueSearch) {
    let timer = null;
    boutiqueSearch.addEventListener('input', (e) => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        const q = (e.target.value || '').toLowerCase().trim();
        document.querySelectorAll('.product-card').forEach(card => {
          const name = (card.dataset.name || '').toLowerCase();
          const desc = (card.dataset.desc || '').toLowerCase();
          const ok = q === '' || name.includes(q) || desc.includes(q);
          card.style.display = ok ? '' : 'none';
        });
      }, 180);
    });
  }

  // Inject floating WhatsApp button for mobile to ensure 'Commander' is always available
  if (!document.getElementById('floatWhatsAppBtn')) {
    const floatBtn = document.createElement('button');
    floatBtn.id = 'floatWhatsAppBtn';
    floatBtn.title = 'Contacter via WhatsApp';
    floatBtn.innerHTML = '<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>';
    document.body.appendChild(floatBtn);
    floatBtn.addEventListener('click', (e) => {
      e.preventDefault();
      // If product modal open, try to read current product title
      const modalOpen = document.querySelector('.product-modal[aria-hidden="false"]');
      let message = 'Bonjour Ro Business Center, je souhaite plus d\'informations.';
      if (modalOpen) {
        const title = document.getElementById('modalTitle')?.textContent?.trim();
        if (title) message = `Bonjour Ro Business Center, je souhaite commander ${title}.`;
      } else {
        // try to find selected product on product detail page
        const pdTitle = document.querySelector('.product-detail-grid h1, .product-page-shell h1');
        if (pdTitle) message = `Bonjour Ro Business Center, je souhaite commander ${pdTitle.textContent.trim()}.`;
      }
      openWhatsApp(message);
    });
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initPage);
} else {
  initPage();
}

window.addEventListener('scroll', () => {
  updateActiveNav();
  toggleScrollTop();
});
