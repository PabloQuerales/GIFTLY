import { useState } from "react";
import Swal from "sweetalert2";

export const Modal = (props) => {
	const [step, setStep] = useState(1);
	const [formData, setFormData] = useState({
		name: "",
		email: "",
		eventType: "",
		participants: 0,
		participantsName: []
	});
	const sendEmail = async () => {
		const myHeaders = new Headers();
		myHeaders.append("Content-Type", "application/json");

		const raw = JSON.stringify({
			organizer_name: formData.name,
			organizer_email: formData.email,
			participantsName: formData.participantsName
		});

		const requestOptions = {
			method: "POST",
			headers: myHeaders,
			body: raw,
			redirect: "follow"
		};

		try {
			const response = await fetch("http://127.0.0.1:5000/send-invitations", requestOptions);
			const result = await response.json();
			console.log(result);
		} catch (error) {
			console.error(error);
		}
	};
	const handleChange = (e, index = null) => {
		const { name, value } = e.target;
		if (name === "participantsName" && index !== null) {
			const updatedParticipants = [...formData.participantsName];
			updatedParticipants[index] = { id: index + 1, name: value };
			setFormData({ ...formData, participantsName: updatedParticipants });
		} else {
			setFormData({ ...formData, [name]: value });
		}
	};
	const handleNext = () => {
		if (step < 5) {
			if (step === 1 && formData.name !== "" && formData.email !== "") {
				setStep(step + 1);
			} else if (step === 2 && formData.eventType !== "") {
				setStep(step + 1);
			} else if (step === 3 && formData.participants > 0) {
				// inicializamos los slots de participantes vacíos al llegar al paso 4
				setFormData({
					...formData,
					participantsName: Array.from({ length: formData.participants }, () => ({ id: null, name: "" }))
				});
				setStep(step + 1);
			} else if (step === 4) {
				const allNamesFilled = formData.participantsName.every((p) => p.name.trim() !== "");
				if (allNamesFilled) {
					sendEmail();
					setStep(step + 1);
				} else {
					Swal.fire({
						title: "Falta Información",
						confirmButtonColor: "#FF6B6B"
					});
				}
			} else {
				Swal.fire({
					title: "Falta Información",
					confirmButtonColor: "#FF6B6B"
				});
			}
		} else {
			setFormData({ name: "", email: "", eventType: "", participants: 0, participantsName: [] });
			setStep(1);
			props.setModalFade(!props.modalFade);
		}
	};
	const handleBack = () => {
		if (step > 1) setStep(step - 1);
	};

	const renderStepContent = () => {
		switch (step) {
			case 1:
				return (
					<div className="flex flex-col justify-center items-center">
						<p className="">Para empezar, te haremos algunas preguntas sencillas que nos ayudarán a crear tu evento de intercambios.</p>

						<label htmlFor="Confirm" className="mt-2 flex flex-col justify-center items-center w-full">
							<span className="font-bold">Comencemos por tu nombre</span>

							<input
								type="text"
								name="name"
								value={formData.name}
								onChange={handleChange}
								required
								placeholder="nombre"
								className="mt-2 p-2 w-1/2 rounded shadow-md sm:text-sm text-black bg-gray-300"
							/>
						</label>
						<label htmlFor="Confirm" className="mt-2 flex flex-col justify-center items-center w-full">
							<span className="font-bold">Tambien necesitamos un correo electrónico para enviarte las invitaciones.</span>

							<input
								type="text"
								name="email"
								value={formData.email}
								onChange={handleChange}
								required
								placeholder="email"
								className="mt-2 p-2 w-1/2 rounded shadow-md sm:text-sm text-black bg-gray-300"
							/>
						</label>
					</div>
				);
			case 2:
				return (
					<div className="flex flex-col justify-center items-center">
						<p>
							<span className="font-bold">{formData.name}</span> que tipo de intercambio estás pensando llevar a cabo?
						</p>
						<div className="flex size-full items-start gap-3 flex-wrap sm:flex-nowrap justify-center">
							<label className="custom-option text-center flex w-1/2 h-full flex-col items-center gap-3 ">
								<div className="flex flex-col">
									<span className=" mb-1 font-bold text-amber-900">Familiar</span>
									<span className="text-xs">Ideal para reuniones de intercambio mas informales, como navidades entre amigos y/o familia. </span>
									<span className="font-bold text-xs">
										Invitados recomendados <br /> entre 3 y 20
									</span>
								</div>
								<input type="checkbox" name="eventType" value="family" onClick={handleChange} className="checkbox checkbox-primary" />
							</label>
							<label className="custom-option text-center flex w-1/2 flex-col items-center gap-3 text-gray-400 cursor-no-drop">
								<span className="flex flex-col">
									<span className="mb-1 font-bold text-amber-900">Laboral</span>
									<span className="text-xs">Ideal para el trabajo y reuniones mas formales con invitaciones por correo electrónico.</span>
									<span className="font-bold text-xs">
										Invitados recomendados <br />
										entre 10 y 20
									</span>
								</span>
								<input type="checkbox" name="eventType" value="labor" onChange={handleChange} className="checkbox checkbox-primary" disabled />
							</label>
						</div>
					</div>
				);
			case 3:
				return (
					<div className="flex flex-col justify-center items-center gap-2	">
						<p>Ahora necesitamos que nos indiques el número de participantes.</p>
						<span className="font-bold">Numero entre 3 y 20</span>
						<div className="input w-1/2">
							<input type="text" name="participants" value={formData.participants} onChange={handleChange} />
							<span className="my-auto flex gap-3">
								<button
									type="button"
									className="btn btn-primary btn-soft size-5.5 min-h-0 rounded-sm p-0"
									onClick={() => {
										formData.participants > 0 ? setFormData({ ...formData, participants: formData.participants - 2 }) : null;
									}}>
									<span className="icon-[tabler--minus] size-3.5 shrink-0"></span>
								</button>
								<button
									type="button"
									className="btn btn-primary btn-soft size-5.5 min-h-0 rounded-sm p-0"
									onClick={() => {
										formData.participants < 16 ? setFormData({ ...formData, participants: formData.participants + 2 }) : null;
									}}>
									<span className="icon-[tabler--plus] size-3.5 shrink-0"></span>
								</button>
							</span>
						</div>
					</div>
				);
			case 4:
				return (
					<div className="flex flex-col w-full h-full">
						<div className="flex flex-col gap-4 w-full items-center">
							<p className="font-bold">Ingresa los nombres de los participantes:</p>
						</div>
						<div className="flex-1 max-h-80 overflow-y-auto mt-4 pr-2">
							<div className="grid grid-cols-2 gap-4">
								{Array.from({ length: formData.participants }).map((_, index) => (
									<div key={index} className="flex flex-col items-center">
										<label className="block text-sm font-medium text-gray-700 mb-1">Participante {index + 1}</label>
										<input
											type="text"
											className="p-2 w-full rounded border border-gray-300 shadow-sm text-black"
											placeholder={`Nombre del participante ${index + 1}`}
											name="participantsName"
											value={formData.participantsName?.[index]?.name || ""}
											onChange={(e) => handleChange(e, index)}
										/>
									</div>
								))}
							</div>
						</div>
					</div>
				);
			case 5:
				return (
					<div className="flex flex-col justify-center items-center gap-4 p-4">
						<h2 className="text-xl font-bold text-amber-900">¡Listo, {formData.name || "Participante"}!</h2>
						<p className="text-center">
							Hemos enviado la información de tu intercambio a tu correo electrónico.
							<span className="font-bold">Recuerda revisar también la bandeja de correos no deseados.</span>
						</p>
						<p className="text-center">
							Por favor, <span className="font-bold">no abras invitaciones que no sean tuyas</span> para no afectar la experiencia de los demás.
							Comparte únicamente las invitaciones con tus amigos o familiares.
						</p>
						<button
							type="button"
							className="mt-4 rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
							onClick={() => props.setModalFade(!props.modalFade)}>
							Cerrar
						</button>
					</div>
				);
			default:
				return null;
		}
	};

	return (
		<div className="w-full text-gray-700 text-sm ms-10 flex flex-col text-center border-l-2 pl-4 h-full">
			<div className="flex items-start justify-center">
				<h2 id="modalTitle" className="text-xl font-bold text-[#FF6B6B] sm:text-2xl">
					Bienvenido a Giftly
				</h2>
			</div>
			<div className="flex-1 m-4 overflow-hidden">{renderStepContent()}</div>
			<footer className="mt-6 flex justify-center gap-2 shrink-0">
				{step !== 5 ? (
					<>
						<button
							type="button"
							onClick={handleBack}
							disabled={step === 1}
							className="rounded bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed">
							Atrás
						</button>
						<button
							type="button"
							className="rounded bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-200"
							onClick={() => props.setModalFade(!props.modalFade)}>
							Cancelar
						</button>
						<button
							type="button"
							onClick={handleNext}
							className="rounded bg-[#FF6B6B] px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-red-300">
							Continuar
						</button>
					</>
				) : (
					<button
						type="button"
						className="rounded bg-[#FF6B6B] px-6 py-2 text-sm font-medium text-white transition-colors hover:bg-red-300"
						onClick={() => props.setModalFade(!props.modalFade)}>
						Gracias
					</button>
				)}
			</footer>
		</div>
	);
};
