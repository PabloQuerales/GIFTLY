export const Steps = () => {
	return (
		<ul className="relative flex h-96 flex-col gap-y-2">
			<li className="group flex flex-1 shrink basis-0 flex-col w-fit">
				<div className="flex items-center justify-center gap-2.5 text-sm">
					<span className="text-bg-soft-neutral size-7.5 flex shrink-0 items-center justify-center rounded-full text-sm font-medium">1</span>
					<div className="text-base-content block">Step</div>
				</div>
				<div className="bg-neutral/20 ms-3.5 mt-2 h-full w-px justify-self-start group-last:hidden"></div>
			</li>

			<li className="group flex flex-1 shrink basis-0 flex-col w-fit">
				<div className="flex items-center justify-center gap-2.5 text-sm">
					<span className="text-bg-soft-neutral size-7.5 flex shrink-0 items-center justify-center rounded-full text-sm font-medium">2</span>
					<div className="text-base-content block">Step</div>
				</div>
				<div className="bg-neutral/20 ms-3.5 mt-2 h-full w-px justify-self-start group-last:hidden"></div>
			</li>

			<li className="group flex flex-1 shrink basis-0 flex-col w-fit">
				<div className="flex items-center justify-center gap-2.5 text-sm">
					<span className="text-bg-soft-neutral size-7.5 flex shrink-0 items-center justify-center rounded-full text-sm font-medium">3</span>
					<div className="text-base-content block">Step</div>
				</div>
				<div className="bg-neutral/20 ms-3.5 mt-2 h-full w-px justify-self-start group-last:hidden"></div>
			</li>
		</ul>
	);
};
